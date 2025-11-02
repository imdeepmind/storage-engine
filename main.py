import os


from db.storage_engine.relation_file import RelationFile

# Test function to generate random data
def generate_random_page():
    return os.urandom(8 * 1024)

relation_file = RelationFile("1234")

# for _ in range(100):
#     relation_file.write_data(generate_random_page())

print("TAIL", relation_file.tail)