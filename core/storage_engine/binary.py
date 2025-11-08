import struct
from decimal import Decimal
from datetime import date, datetime, timedelta
import re


def pack_row(row: dict, columns: list[tuple[str, str]]) -> bytes:
    """
    Packs a row dict into binary form based on the column definitions.

    Args:
        row: dict containing column_name -> value
        columns: list of tuples like [(col_name, col_type), ...]

    Returns:
        bytes: binary representation of the row
    """
    format_str = "<"  # little-endian
    values = []

    for col_name, col_type in columns:
        value = row.get(col_name)

        if value is None:
            raise ValueError(f"Missing value for column '{col_name}'")

        col_type = col_type.lower().strip()

        # Extract base type and optional length
        match = re.match(r"([a-z]+)(?:\((\d+)\))?", col_type)
        if not match:
            raise TypeError(f"Invalid column type: {col_type}")

        base_type = match.group(1)
        length = int(match.group(2)) if match.group(2) else None

        if base_type == "integer":
            format_str += "q"
            values.append(int(value))

        elif base_type == "decimal":
            format_str += "d"
            values.append(float(Decimal(value)))

        elif base_type == "varchar":
            if length is None:
                raise ValueError(f"VARCHAR column '{col_name}' requires length")
            encoded = value.encode("utf-8")
            if len(encoded) > length:
                raise ValueError(
                    f"Value too long for column '{col_name}' (max {length})"
                )
            format_str += f"{length}s"
            values.append(encoded.ljust(length, b"\x00"))

        elif base_type == "text":
            encoded = value.encode("utf-8")
            length = len(encoded)
            format_str += f"I{length}s"
            values.append(length)
            values.append(encoded)

        elif base_type == "bool":
            format_str += "?"
            values.append(bool(value))

        elif base_type == "date":
            if isinstance(value, str):
                value = date.fromisoformat(value)
            days_since_epoch = (value - date(1970, 1, 1)).days
            format_str += "i"
            values.append(days_since_epoch)

        elif base_type == "datetime":
            if isinstance(value, str):
                value = datetime.fromisoformat(value)
            timestamp = int(value.timestamp())
            format_str += "q"
            values.append(timestamp)

        else:
            raise TypeError(f"Unsupported column type: {col_type}")

    return struct.pack(format_str, *values)


def unpack_row(raw_data: bytes, columns: list[tuple[str, str]]) -> dict:
    """
    Deserialize raw binary tuple data into Python dictionary based on columns.

    Args:
        raw_data (bytes): Binary data for the tuple.
        columns (list[tuple]): List of (name, type)
            Example: [("id", "integer"), ("price", "decimal"), ("name", "varchar(20)")]

    Returns:
        dict: {column_name: value}
    """
    format_parts = []

    parsed_columns = []
    for col_name, col_type in columns:
        col_type = col_type.lower().strip()

        match = re.match(r"([a-z]+)(?:\((\d+)\))?", col_type)
        if not match:
            raise TypeError(f"Invalid column type: {col_type}")

        base_type = match.group(1)
        length = int(match.group(2)) if match.group(2) else None

        if base_type == "integer":
            fmt = "q"
        elif base_type == "decimal":
            fmt = "d"
        elif base_type == "varchar":
            if length is None:
                raise ValueError(f"VARCHAR column '{col_name}' requires length")
            fmt = f"{length}s"
        elif base_type == "text":
            fmt = "I"  # we’ll read the text length first, then slice manually
        elif base_type == "bool":
            fmt = "?"
        elif base_type == "date":
            fmt = "i"
        elif base_type == "datetime":
            fmt = "q"
        else:
            raise TypeError(f"Unsupported column type: {col_type}")

        format_parts.append(fmt)
        parsed_columns.append((col_name, base_type, length))

    # First unpack fixed-length types
    struct_format = "<" + "".join(format_parts)
    header_size = struct.calcsize(struct_format)
    unpacked = list(struct.unpack(struct_format, raw_data[:header_size]))

    result = {}
    offset = header_size

    for i, (col_name, base_type, length) in enumerate(parsed_columns):
        val = unpacked[i]

        if base_type == "varchar":
            val = val.rstrip(b"\x00").decode("utf-8")
        elif base_type == "decimal":
            val = Decimal(str(val))
        elif base_type == "date":
            val = date(1970, 1, 1) + timedelta(days=val)
        elif base_type == "datetime":
            val = datetime.fromtimestamp(val)
        elif base_type == "text":
            text_len = val
            text_bytes = struct.unpack_from(f"{text_len}s", raw_data, offset)[0]
            offset += text_len
            val = text_bytes.decode("utf-8")

        result[col_name] = val

    return result
