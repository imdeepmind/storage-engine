from core.storage_engine.file_manager import FileStorage

FileStorage.create_folder_if_not_exists("./data/test/another/test")
FileStorage.create_empty_file("./data/test/another/test", "data.pydb")