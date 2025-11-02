import os

from .file_manager import FileStorage


class Relation:
    RELATION_FILE = "data1.pydb"

    def __init__(self, table_id):
        self.folder = os.path.join("./data", table_id)
        self.path = os.path.join(self.folder, self.RELATION_FILE)

    def create_relation(self):
        FileStorage.create_folder_if_not_exists(self.folder)
        FileStorage.create_empty_file(self.folder, self.RELATION_FILE)

    def write_data(self, page_data, offset=0):
        with open(self.path, "w+b") as f:
            f.seek(offset)
            f.write(page_data)
            f.flush()
            os.fsync(f.fileno())
