"""Exceptions module for the storage engine."""

from .storage_exceptions import (
    StorageException,
    FileAccessError,
    FileNotFoundError,
    FileCorruptionError,
    DirectoryAccessError,
)

__all__ = [
    "StorageException",
    "FileAccessError",
    "FileNotFoundError",
    "FileCorruptionError",
    "DirectoryAccessError",
]