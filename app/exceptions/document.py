"""
Document-related exceptions.
"""

from app.exceptions.base import AppError


class DocumentError(AppError):
    """Base document exception."""


class DocumentNotFoundError(DocumentError):
    """Document does not exist."""


class CorruptedDocumentError(DocumentError):
    """Document cannot be parsed."""


class EmptyDocumentError(DocumentError):
    """Document contains no readable content."""
