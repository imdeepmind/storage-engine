import os

from core.utils import logger
from core.exceptions import FileAccessError, FileNotFoundError, DirectoryAccessError

class FileStorage:
    """A class for handling file storage operations such as creating folders, writing data, and reading data."""

    @staticmethod
    def create_folder_if_not_exists(folder_name):
        """Create a folder if it does not exist.

        Args:
            folder_name (str): The name of the folder to create.

        Returns:
            str: The name of the folder.

        Raises:
            DirectoryAccessError: If the directory cannot be created due to permissions or other OS errors.
        """
        logger.debug(f"FileStorage: Creating folder {folder_name}")
        try:
            os.makedirs(folder_name, exist_ok=True)
            return folder_name
        except OSError as e:
            raise DirectoryAccessError(f"Failed to create directory {folder_name}: {e}")

    @staticmethod
    def write_data(path, data, offset=0):
        """Write data to a file at a specified offset.

        Args:
            path (str): The file path to write to.
            data (bytes): The data to write.
            offset (int, optional): The offset to start writing from. Defaults to 0.

        Raises:
            FileAccessError: If there are permission issues or OS errors during writing.
            FileNotFoundError: If the file path is invalid.
        """
        logger.debug(f"FileStorage: Write to file {path} with offset {offset}")
        try:
            mode = "r+b" if os.path.exists(path) else "w+b"
            with open(path, mode) as f:
                f.seek(offset)
                f.write(data)
                f.flush()
                os.fsync(f.fileno())
        except PermissionError:
            raise FileAccessError(f"Permission denied for file {path}")
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {path}")
        except OSError as e:
            raise FileAccessError(f"OS error writing to {path}: {e}")

    @staticmethod
    def read_data(path, offset=0, size=-1):
        """Read data from a file.

        Args:
            path (str): The file path to read from.
            offset (int, optional): The offset to start reading from. Defaults to 0 (beginning).
            size (int, optional): The number of bytes to read. Defaults to -1 (entire file).

        Returns:
            bytes: The read data.

        Raises:
            FileAccessError: If there are permission issues or OS errors during reading.
            FileNotFoundError: If the file does not exist.
        """
        logger.debug(f"FileStorage: Reading file {path} from offset {offset}, size {size}")
        try:
            with open(path, "rb") as f:
                if offset >= 0:
                    f.seek(offset)         # move file pointer to the given offset
                if size > 0:
                    return f.read(size)    # read 'size' bytes from that position
                return f.read()            # read entire file
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {path}")
        except PermissionError:
            raise FileAccessError(f"Permission denied for file {path}")
        except OSError as e:
            raise FileAccessError(f"OS error reading from {path}: {e}")
