import ulid
import os

from core.storage_engine.relation import Relation
from core.constants import PAGE_SIZE


relation = Relation(ulid.ulid())
relation.create_relation()
print(relation.read_metadata())
relation.write_data(os.urandom(PAGE_SIZE))
