PAGE_SIZE = 8 * 1024
META_FORMAT = (
    "<HHIQQQ"  # version, page_size, segment_count, total_pages, tail, created_at
)
RELATION_FILE_VERSION = 1
RELATION_METADATA_FILE_NAME = "metadata.pydb"