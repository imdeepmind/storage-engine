import os

from core.utils import logger
from core.constants import PAGE_SIZE

class FileStorage:
    @staticmethod
    def create_folder_if_not_exists(folder_name):
        logger.debug(f"FileStorage: Creating folder {folder_name}")
        os.makedirs(folder_name, exist_ok=True)
        return folder_name

    @staticmethod
    def write_data(path, data, offset=0):
        logger.debug(f"FileStorage: Write to file {path} with offset {offset}")
        with open(path, "w+b") as f:
            f.seek(offset)
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

    @staticmethod
    def read_data(path, offset=-1, size=-1):
        logger.debug(f"FileStorage: Reading file {path} from offset {offset}, size {size}")
        with open(path, "rb") as f:
            if offset >= 0:
                f.seek(offset)         # move file pointer to the given offset
            if size > 0:
                return f.read(size)    # read 'size' bytes from that position
            return f.read()            # read entire file
