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

from core.exceptions import FileAccessError, FileNotFoundError, DirectoryAccessError

from .file_manager import FileStorage


class Relation:
    """Represents a database relation (table) in the storage engine.

    This class manages the storage and retrieval of data and metadata for a specific table.
    It handles file operations for relation data files and their associated metadata files.
    """

    # TODO: Need to support multiple relation files
    RELATION_FILE = "data1.pydb"

    def __init__(self, table_id):
        """Initialize a Relation instance for a specific table.

        Sets up the file paths for the relation data file and metadata file based on the table ID.

        Args:
            table_id (str): The unique identifier for the table, used to create the folder structure.
        """
        self.folder = os.path.join("./data", table_id)
        self.path = os.path.join(self.folder, self.RELATION_FILE)
        self.metadata = os.path.join(self.folder, RELATION_METADATA_FILE_NAME)

    def create_relation(self):
        """Create a new relation by setting up the necessary folder structure and initial metadata.

        This method creates the data folder for the table if it doesn't exist and initializes
        the metadata file with default values (0 total pages, tail page ID 0).
        """
        logger.debug("Relation: Creating a new Relation")
        try:
            FileStorage.create_folder_if_not_exists(self.folder)
            self.write_metadata(0, 0)
        except (DirectoryAccessError, FileAccessError, FileNotFoundError) as e:
            logger.error(f"Failed to create relation for table {self.folder}: {e}")
            raise RuntimeError(
                f"Unrecoverable error: Failed to create relation for table {self.folder}: {e}"
            )

    def write_data(self, page_data, offset=0):
        """Write binary data to the relation file at the specified offset.

        This method writes binary data to the relation's data file, allowing for appending
        or overwriting data at specific positions within the file.

        Args:
            page_data (bytes): The binary data to write.
            offset (int, optional): The byte offset in the file to start writing from. Defaults to 0.

        Returns:
            None
        """
        logger.debug(f"Relation: Writing to relation file with offset {offset}")
        try:
            return FileStorage.write_data(self.path, page_data, offset)
        except (FileAccessError, FileNotFoundError) as e:
            logger.error(f"Failed to write data to relation file {self.path}: {e}")
            raise RuntimeError(
                f"Unrecoverable error: Failed to write data to relation file {self.path}: {e}"
            )

    def write_metadata(self, total_pages, tail_page_id):
        """Write metadata information for the relation to its metadata file.

        The metadata includes version, page size, segment count, total pages, tail page ID,
        and creation timestamp. This information is packed into binary format and written
        to the metadata file.

        Args:
            total_pages (int): The total number of pages currently in the relation.
            tail_page_id (int): The ID of the last (tail) page in the relation.

        Returns:
            None
        """
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
        try:
            return FileStorage.write_data(self.metadata, data)
        except (FileAccessError, FileNotFoundError) as e:
            logger.error(f"Failed to write metadata to {self.metadata}: {e}")
            raise RuntimeError(
                f"Unrecoverable error: Failed to write metadata to {self.metadata}: {e}"
            )

    def read_metadata(self):
        """Read and unpack metadata from the relation's metadata file.

        Retrieves the binary metadata and unpacks it into a tuple containing relation information.

        Returns:
            tuple: A tuple containing (version, page_size, segment_count, total_pages, tail_page_id, created_at).
                - version (int): The file format version.
                - page_size (int): The size of each page in bytes.
                - segment_count (int): Number of file segments (currently fixed at 1).
                - total_pages (int): Total number of pages in the relation.
                - tail_page_id (int): ID of the last page.
                - created_at (int): Unix timestamp when the relation was created.

        Raises:
            FileCorruptionError: If the metadata file is corrupted or has invalid format.
        """
        logger.debug("Relation: Reading the relation metadata")
        try:
            raw = FileStorage.read_data(self.metadata)
            return struct.unpack(META_FORMAT, raw)
        except (FileAccessError, FileNotFoundError) as e:
            logger.error(f"Failed to read metadata from {self.metadata}: {e}")
            raise RuntimeError(
                f"Unrecoverable error: Failed to read metadata from {self.metadata}: {e}"
            )
        except struct.error as e:
            logger.error(f"Metadata file {self.metadata} is corrupted: {e}")
            raise RuntimeError(
                f"Unrecoverable error: Metadata file {self.metadata} is corrupted: {e}"
            )
