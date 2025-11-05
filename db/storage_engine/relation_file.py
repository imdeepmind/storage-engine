import os
import struct
import time

PAGE_SIZE = 8 * 1024  # 8KB
RELATION_FILE_MAZ_SIZE = 100 * 1024  # 100KB
RELATION_FILE_FOLDER = "relation_files"
META_FORMAT = (
    "<HHIQQQ"  # version, page_size, segment_count, total_pages, tail_page_id, created_at
)
VERSION = 1


class RelationFile:
    tail = 0
    offset_in_relation = 4

    def __init__(self, table_id):
        self._table_id = table_id
        self._path = os.path.join(RELATION_FILE_FOLDER, self._table_id)

        # create the table folder
        self.__create_table_folder_if_needed()

        self.__create_relation_file()

    def __create_table_folder_if_needed(self):
        folder_path = os.path.join(RELATION_FILE_FOLDER, str(self._table_id))
        os.makedirs(folder_path, exist_ok=True)

    def __create_relation_file(self):
        # TODO: Need to handle multiple relation files
        relation_file = os.path.join(self._path, "data1.pydb")

        if os.path.exists(relation_file):
            return

        with open(relation_file, "wb") as f:
            f.write(b"")
            f.flush()
            os.fsync(f.fileno())

        self.__write_metadata()

        return

    def __total_number_of_data_files(self):
        return len(list(filter(lambda x: x.startswith("data"), os.listdir(self._path))))

    def __write_metadata(self):
        with open(os.path.join(self._path, "metadata.pydb"), "r+b") as f:
            data = struct.pack(
                META_FORMAT,
                VERSION,
                PAGE_SIZE,
                self.__total_number_of_data_files(),
                0,
                0,
                int(time.time()),
            )
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        return

    def __read_metadata(self):
        with open(self._relation_file, "rb") as f:
            raw = f.read(self.offset_in_relation)
            return struct.unpack("<I", raw)[0]

    def write_data(self, page_data):
        with open(self._relation_file, "w+b") as f:
            offset = (self.tail * PAGE_SIZE) + self.offset_in_relation

            f.seek(offset)
            f.write(page_data)
            f.flush()
            os.fsync(f.fileno())

            self.tail += 1

            self.__write_metadata()

        return
