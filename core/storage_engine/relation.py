import os
import time
import struct

from core.constants import (
    META_FORMAT,
    RELATION_FILE_VERSION,
    PAGE_SIZE,
    RELATION_METADATA_FILE_NAME,
)
from core.utils import logger

from .file_manager import FileStorage


class Relation:
    RELATION_FILE = "data1.pydb"

    def __init__(self, table_id):
        self.folder = os.path.join("./data", table_id)
        self.path = os.path.join(self.folder, self.RELATION_FILE)
        self.metadata = os.path.join(self.folder, RELATION_METADATA_FILE_NAME)

    def create_relation(self):
        logger.debug("Relation: Creating a new Relation")
        FileStorage.create_folder_if_not_exists(self.folder)
        self.write_metadata(0, 0)

    def write_data(self, page_data, offset=0):
        logger.debug(f"Relation: Writing to relation file with offset {offset}")
        return FileStorage.write_data(self.path, page_data, offset)

    def write_metadata(self, total_pages, tail_page_id):
        logger.debug(
            f"Relation: Writing relation metadata with total_pages as {total_pages} and tail_page_id as {tail_page_id}"
        )
        data = struct.pack(
            META_FORMAT,
            RELATION_FILE_VERSION,  # version
            PAGE_SIZE,  # page_size
            1,  # TODO: Need to update this to support multiple relation files, segment_count
            total_pages,  # total_pages
            tail_page_id,  # tail_page_id
            int(time.time()),  # created_at
        )

        return FileStorage.write_data(self.metadata, data)

    def read_metadata(self):
        logger.debug("Relation: Reading the relation metadata")
        raw = FileStorage.read_data(self.metadata)
        return struct.unpack(META_FORMAT, raw)
