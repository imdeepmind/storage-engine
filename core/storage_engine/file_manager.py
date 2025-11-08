import os

from core.utils import logger

class FileStorage:
    """A class for handling file storage operations such as creating folders, writing data, and reading data."""

    @staticmethod
    def create_folder_if_not_exists(folder_name):
        """Create a folder if it does not exist.

        Args:
            folder_name (str): The name of the folder to create.

        Returns:
            str: The name of the folder.
        """
        logger.debug(f"FileStorage: Creating folder {folder_name}")
        os.makedirs(folder_name, exist_ok=True)
        return folder_name

    @staticmethod
    def write_data(path, data, offset=0):
        """Write data to a file at a specified offset.

        Args:
            path (str): The file path to write to.
            data (bytes): The data to write.
            offset (int, optional): The offset to start writing from. Defaults to 0.
        """
        logger.debug(f"FileStorage: Write to file {path} with offset {offset}")
        mode = "r+b" if os.path.exists(path) else "w+b"
        with open(path, mode) as f:
            f.seek(offset)
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

    @staticmethod
    def read_data(path, offset=-1, size=-1):
        """Read data from a file.

        Args:
            path (str): The file path to read from.
            offset (int, optional): The offset to start reading from. Defaults to -1 (beginning).
            size (int, optional): The number of bytes to read. Defaults to -1 (entire file).

        Returns:
            bytes: The read data.
        """
        logger.debug(f"FileStorage: Reading file {path} from offset {offset}, size {size}")
        with open(path, "rb") as f:
            if offset >= 0:
                f.seek(offset)         # move file pointer to the given offset
            if size > 0:
                return f.read(size)    # read 'size' bytes from that position
            return f.read()            # read entire file
