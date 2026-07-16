"""
Reader-related exceptions.
"""

from app.exceptions.base import AppError


class ReaderError(AppError):
    """Base reader exception."""


class UnsupportedDocumentTypeError(ReaderError):
    """No reader supports this document."""
