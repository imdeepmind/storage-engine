import ulid
import os

from core.storage_engine.page import Page
# from core.constants import PAGE_SIZE


page = Page(ulid.ulid())
print("===============")
page.write_tuple_data(os.urandom(100))
print("===============")
page.write_tuple_data(os.urandom(100))
print("===============")
# page.write_tuple_data(os.urandom(100))
# print("===============")