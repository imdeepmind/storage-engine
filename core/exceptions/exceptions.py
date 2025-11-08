"""Custom exceptions for the storage engine."""


class StorageException(Exception):
    """Base exception for storage-related errors."""
    pass


class FileAccessError(StorageException):
    """Raised when there is an issue accessing a file (permissions, path invalid, etc.)."""
    pass


class FileNotFoundError(StorageException):
    """Raised when a required file is not found."""
    pass


class FileCorruptionError(StorageException):
    """Raised when a file appears to be corrupted or has invalid data."""
    pass


class DirectoryAccessError(StorageException):
    """Raised when there is an issue accessing or creating directories."""
    pass

class CurrentlyNotSupported(StorageException):
    """Raised when some feature is not yet supported"""
    pass
