import os
import struct

PAGE_SIZE = 8 * 1024 # 8KB
RELATION_FILE_MAZ_SIZE = 100 * 1024 # 100KB
RELATION_FILE_FOLDER = "relation_files"

class RelationFile:
    tail = 0
    offset_in_relation = 4

    def __init__(self, relation_file):
        self._relation_file = os.path.join(RELATION_FILE_FOLDER, relation_file)
        
        self.__create_relation_file()
        self.tail = self.__read_metadata()
    
    def __create_relation_file(self):
        if os.path.exists(self._relation_file):
            return
        
        with open(self._relation_file, "wb") as f:
            f.write(b"")
            f.flush()
            os.fsync(f.fileno())
            
        self.__write_metadata()

        return
    
    def __write_metadata(self):
        with open(self._relation_file, "r+b") as f:
            data = struct.pack("<I", self.tail)
            
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


# Test function to generate random data
def generate_random_page():
    return os.urandom(PAGE_SIZE)

relation_file = RelationFile("001.dat")

for _ in range(100):
    relation_file.write_data(generate_random_page())

print("TAIL", relation_file.tail)