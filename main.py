import ulid
import datetime
from decimal import Decimal

from core.storage_engine import Tuple
# from core.constants import PAGE_SIZE


tuple = Tuple(ulid.ulid())
print("===============")

columns = [
    ("id", "INTEGER"),
    ("price", "DECIMAL"),
    ("name", "VARCHAR(20)"),
    ("active", "BOOL"),
    ("created_at", "DATETIME"),
]

row = {
    "id": 42,
    "price": Decimal("19.99"),
    "name": "Abhishek",
    "active": True,
    "created_at": datetime.datetime(2025, 10, 28, 12, 0, 0),
}

row2 = {
    "id": 423,
    "price": Decimal("19.99"),
    "name": "Abhishek",
    "active": True,
    "created_at": datetime.datetime(2025, 10, 28, 12, 0, 0),
}
page_id1, slot_id1 = tuple.write_tuple(row, columns)
page_id2, slot_id2 = tuple.write_tuple(row2, columns)

print("======READING FIRST PAGE=====")
print(tuple.read_tuple(page_id1, slot_id1, columns))
print("======")
print("======READING SECOND PAGE=====")
print(tuple.read_tuple(page_id2, slot_id2, columns))
print("======")
