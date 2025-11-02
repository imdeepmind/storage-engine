import os


class FileStorage:
    @staticmethod
    def create_folder_if_not_exists(folder_name):
        os.makedirs(folder_name, exist_ok=True)
        return folder_name

    @staticmethod
    def create_empty_file(folder_path, file_name):
        path = os.path.join(folder_path, file_name)

        with open(path, "wb") as f:
            f.write(b"")
            f.flush()
            os.fsync(f.fileno())

        return

    @staticmethod
    def write_data(path, data, offset=0):
        with open(path, "w+b") as f:
            f.seek(offset)
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
