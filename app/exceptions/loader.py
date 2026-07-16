"""
Loader-related exceptions.
"""

from app.exceptions.base import AppError


class LoaderError(AppError):
    """Base loader exception."""


class UnsupportedLoaderError(LoaderError):
    """No loader registered for the supplied file type."""
