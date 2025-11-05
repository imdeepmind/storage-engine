class Tuple:
    def __init__(self):
        pass

    def read_tuple(self, table_id, page_id, slot_no):
        pass

    def write_tuple(self, table_id, record: dict):
        # get the last page where we can fit data
        # if the last page cant fit the data (there is no space), then create new page
        # then insert the record in page
        # update metadata
        pass

    def update_tuple(self, table_id, page_id, slot_id, record: dict):
        pass

    def delete_tuple(self, table_id, page_id, slot_id):
        pass
