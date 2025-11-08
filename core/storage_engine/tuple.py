from typing import List

from .page import Page
from .binary import pack_row, unpack_row


class Tuple:
    def __init__(self, table_id):
        self.page = Page(table_id)

    def read_tuple(self, page_id, slot_id, columns):
        page_data = self.page.read_page(page_id)
        raw_data = page_data[7]

        return unpack_row(raw_data[slot_id:], columns)

    def write_tuple(self, record: dict, columns: List[dict]):
        return self.page.write_page(pack_row(record, columns))

    def update_tuple(self, table_id, page_id, slot_id, record: dict):
        pass

    def delete_tuple(self, table_id, page_id, slot_id):
        pass
