# Common
PAGE_SIZE = 8 * 1024

# Relation
META_FORMAT = "<HHIQQQ"  # version, page_size, segment_count, total_pages, tail_page_id, created_at
RELATION_FILE_VERSION = 1
RELATION_METADATA_FILE_NAME = "metadata.pydb"

# Page
PAGE_HEADER_FORMAT = (
    "<IHHHIQ"  # page_id, lower, upper, free_space, tuple_count, created_at
)
SLOT_FORMAT = "<H"  # 2 bytes offset to tuple start
