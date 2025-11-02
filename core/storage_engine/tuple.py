class Tuple:
    def __init__(self):
        pass

    def read_tuple(self, table_id, page_id, slot_no):
        pass

    def write_tuple(self, table_id, record: dict):
        pass

    def update_tuple(self, table_id, page_id, slot_id, record: dict):
        pass

    def delete_tuple(self, table_id, page_id, slot_id):
        pass
