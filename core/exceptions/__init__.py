"""Exceptions module for the storage engine."""

from .exceptions import (
    StorageException,
    FileAccessError,
    FileNotFoundError,
    FileCorruptionError,
    DirectoryAccessError,
    CurrentlyNotSupported,
)

__all__ = [
    "StorageException",
    "FileAccessError",
    "FileNotFoundError",
    "FileCorruptionError",
    "DirectoryAccessError",
    "CurrentlyNotSupported",
]