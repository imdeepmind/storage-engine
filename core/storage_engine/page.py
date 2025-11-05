import time
import struct

from core.constants import PAGE_HEADER_FORMAT, PAGE_SIZE, SLOT_FORMAT

from .file_manager import FileStorage
from .relation import Relation

PAGE_HEADER_SIZE = struct.calcsize(PAGE_HEADER_FORMAT)
SLOT_SIZE = struct.calcsize(SLOT_FORMAT)


class Page:
    def __init__(self, table_id):
        self.relation = Relation(table_id)
        self.relation.create_relation()

    def __get_metadata(
        self, page_id, lower=PAGE_HEADER_SIZE, upper=PAGE_SIZE, tuple_count=0
    ):
        header_data = struct.pack(
            PAGE_HEADER_FORMAT,
            page_id,
            lower,  # offset where slot array ends (start of free space)
            upper,  # offset where free space ends (start of tuple data)
            upper - lower,  # free_space
            tuple_count,  # tuple_count
            int(time.time()),  # created_at
        )

        return header_data

    def __get_empty_page(self, tail_page_id=-1):
        page_id = tail_page_id + 1
        page = bytearray(PAGE_SIZE)

        # empty metadata
        page[0:PAGE_HEADER_SIZE] = self.__get_metadata(page_id)

        return page

    def read_page(self, page_id, raw_page=None):
        if not raw_page:
            raw_page = FileStorage.read_data(self.relation.path, page_id * PAGE_SIZE)

        header = struct.unpack(PAGE_HEADER_FORMAT, raw_page[:PAGE_HEADER_SIZE])
        page_id, lower, upper, free_space, tuple_count, created_at = header

        slots = []
        slow_area_size = lower - PAGE_HEADER_SIZE
        num_slots = slow_area_size // SLOT_SIZE

        for i in range(num_slots):
            slot_offset = PAGE_HEADER_SIZE + (i * SLOT_SIZE)
            (tuple_offset,) = struct.unpack(SLOT_FORMAT, raw_page, slot_offset)

            slots.append(tuple_offset)

        return (
            page_id,
            lower,
            upper,
            free_space,
            tuple_count,
            created_at,
            slots,
            raw_page,
        )

    def write_tuple_data(self, tuple_data):
        # get total_pages and tail_page_id
        metadata = self.relation.read_metadata()
        total_pages = metadata[3]
        tail_page_id = metadata[4]

        # if there is no page, initialize a empty page
        if total_pages <= 0:
            page_data = self.read_page(
                tail_page_id, self.__get_empty_page(tail_page_id)
            )
        else:
            page_data = self.read_page(tail_page_id)

        (
            page_id,
            lower,
            upper,
            free_space,
            tuple_count,
            created_at,
            slots,
            page,
        ) = page_data

        tuple_size = len(tuple_data)
        needed_space = tuple_size + SLOT_SIZE

        if free_space >= needed_space:
            # we can fit the data in the page
            new_upper = upper - tuple_size
            new_lower = lower + SLOT_SIZE

            # data
            page[new_upper:upper] = tuple_data

            # header
            header = self.__get_metadata(
                tail_page_id, new_lower, new_upper, tuple_count
            )
            page[:PAGE_HEADER_SIZE] = header

            # slots
            struct.pack_into(SLOT_FORMAT, page, lower, new_upper)

            self.relation.write_data(page, tail_page_id * PAGE_SIZE)
        else:
            # create a new page
            pass
