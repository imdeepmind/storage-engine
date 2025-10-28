import os

PAGE_SIZE = 8 * 1024 # 8KB
RELATION_FILE_MAZ_SIZE = 100 * 1024 # 100KB
RELATION_FILE_FOLDER = "relation_files"

class RelationFile:
    def __init__(self, relation_file):
        self._relation_file = os.path.join(RELATION_FILE_FOLDER, relation_file)
        
        self.__create_relation_file()
    
    def __create_relation_file(self):
        if os.path.exists(self._relation_file):
            return
        
        with open(self._relation_file, "wb") as f:
            f.write(b"")
            f.flush()
            os.fsync(f.fileno())

        return

relation_file = RelationFile("001.dat")