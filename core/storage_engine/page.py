import time
import struct

from core.constants import PAGE_HEADER_FORMAT, PAGE_SIZE, SLOT_FORMAT
from core.utils import logger
from core.exceptions import CurrentlyNotSupported

from .file_manager import FileStorage
from .relation import Relation

PAGE_HEADER_SIZE = struct.calcsize(PAGE_HEADER_FORMAT)
SLOT_SIZE = struct.calcsize(SLOT_FORMAT)


class Page:
    """Represents a page in the storage engine for managing tuple data.

    This class handles the creation, reading, and writing of pages within a relation.
    A page contains a header with metadata, a slot array for tuple offsets, and the actual tuple data.
    """

    def __init__(self, table_id):
        """Initialize a Page instance for a specific table.

        Creates a new relation for the table if it doesn't exist.

        Args:
            table_id (str): The unique identifier for the table.
        """
        self.relation = Relation(table_id)
        self.relation.create_relation()

    def __get_metadata(
        self, page_id, lower=PAGE_HEADER_SIZE, upper=PAGE_SIZE, tuple_count=0
    ):
        """Generate formatted metadata for a page header.

        Args:
            page_id (int): The unique identifier for the page.
            lower (int, optional): Offset where the slot array ends. Defaults to PAGE_HEADER_SIZE.
            upper (int, optional): Offset where free space ends. Defaults to PAGE_SIZE.
            tuple_count (int, optional): Number of tuples in the page. Defaults to 0.

        Returns:
            bytes: Packed header data.
        """
        logger.debug(
            f"Page: Getting formatted metadata with page_id={page_id}, lower={lower}, upper={upper}, tuple_count={tuple_count}"
        )
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
        """Create an empty page with initialized header.

        Args:
            tail_page_id (int, optional): The ID of the last page. Defaults to -1.

        Returns:
            bytearray: An empty page with header initialized.
        """
        logger.debug(f"Page: Getting an empty page with tail_page_id={tail_page_id}")
        page_id = tail_page_id + 1
        page = bytearray(PAGE_SIZE)

        # empty metadata
        page[0:PAGE_HEADER_SIZE] = self.__get_metadata(page_id)

        return page

    def __write_to_new_page(
        self,
        tuple_data,
        tail_page_id,
        lower,
        upper,
        tuple_count,
        page,
        tuple_size,
        total_pages,
    ):
        """Write tuple data to a new page and update metadata.

        Args:
            tuple_data (bytes): The tuple data to write.
            tail_page_id (int): The ID of the tail page.
            lower (int): Current lower offset.
            upper (int): Current upper offset.
            tuple_count (int): Current tuple count.
            page (bytearray): The page buffer.
            tuple_size (int): Size of the tuple data.
            total_pages (int): Total number of pages.
        """
        new_upper = upper - tuple_size
        new_lower = lower + SLOT_SIZE

        # data
        page[new_upper:upper] = tuple_data

        # header
        header = self.__get_metadata(tail_page_id, new_lower, new_upper, tuple_count)
        page[:PAGE_HEADER_SIZE] = header

        # slots
        struct.pack_into(SLOT_FORMAT, page, lower, new_upper)

        self.relation.write_data(page, tail_page_id * PAGE_SIZE)
        self.relation.write_metadata(total_pages, tail_page_id)

    def read_page(self, page_id, raw_page=None):
        """Read and parse a page from the relation file.

        Args:
            page_id (int): The ID of the page to read.
            raw_page (bytes, optional): Raw page data if already available. Defaults to None.

        Returns:
            tuple: A tuple containing (page_id, lower, upper, free_space, tuple_count, created_at, slots, page_data).
        """
        logger.debug(f"Page: Reading page from file or stream with page_id={page_id}")
        if not raw_page:
            raw_page = FileStorage.read_data(
                self.relation.path, page_id * PAGE_SIZE, PAGE_SIZE
            )

        header = struct.unpack(PAGE_HEADER_FORMAT, raw_page[:PAGE_HEADER_SIZE])
        page_id, lower, upper, free_space, tuple_count, created_at = header

        slots = []
        slow_area_size = lower - PAGE_HEADER_SIZE
        num_slots = slow_area_size // SLOT_SIZE

        for i in range(num_slots):
            slot_offset = PAGE_HEADER_SIZE + (i * SLOT_SIZE)
            (tuple_offset,) = struct.unpack_from(SLOT_FORMAT, raw_page, slot_offset)

            slots.append(tuple_offset)

        return (
            page_id,
            lower,
            upper,
            free_space,
            tuple_count,
            created_at,
            slots,
            bytearray(raw_page),
        )

    def write_page(self, tuple_data):
        """Write tuple data to an appropriate page in the relation.

        This method handles page allocation and writing tuple data, creating new pages as needed.

        Args:
            tuple_data (bytes): The tuple data to write.

        Raises:
            CurrentlyNotSupported: If the tuple is too large for a single page.
        """
        logger.debug("Page: Writing new tuple data")
        # get total_pages and tail_page_id
        metadata = self.relation.read_metadata()
        total_pages = metadata[3]
        tail_page_id = metadata[4]
        tuple_size = len(tuple_data)
        needed_space = tuple_size + SLOT_SIZE

        if needed_space > (PAGE_SIZE - PAGE_HEADER_SIZE - SLOT_SIZE):
            raise CurrentlyNotSupported(
                "Large tuples that are bigger the page cannot be saved, this feature will come in future."
            )

        # if there is no page, initialize a empty page
        if total_pages <= 0:
            logger.debug("Page: There is no existing page, getting a page")
            total_pages += 1
            page_data = self.read_page(tail_page_id, self.__get_empty_page())
        else:
            page_data = self.read_page(tail_page_id)

        if needed_space > page_data[3]:
            total_pages += 1
            page_data = self.read_page(
                tail_page_id, self.__get_empty_page(tail_page_id)
            )

        (
            page_id,
            lower,
            upper,
            _,
            tuple_count,
            _,
            _,
            page,
        ) = page_data

        self.__write_to_new_page(
            tuple_data,
            page_id,
            lower,
            upper,
            tuple_count,
            page,
            tuple_size,
            total_pages,
        )
        self.relation.write_metadata(total_pages, tail_page_id)
