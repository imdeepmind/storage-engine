import os

from utils import logger

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
    def read_data(path, offset=-1):
        logger.debug(f"FileStorage: Reading file {path} with offset {offset}")
        with open(path, "rb") as f:
            if offset >= 0:
                return f.read(offset)

            return f.read()
