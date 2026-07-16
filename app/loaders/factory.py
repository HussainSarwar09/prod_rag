"""
Factory responsible for selecting the appropriate document loader.
"""

from pathlib import Path

from app.core.interfaces.document_loader import DocumentLoader
from app.exceptions.loader import UnsupportedLoaderError


class LoaderFactory:
    """
    Selects the appropriate loader implementation.
    """

    def __init__(self, loaders: list[DocumentLoader]) -> None:
        self._loaders = loaders

    def get_loader(self, file_path: Path) -> DocumentLoader:
        """
        Return the first loader that supports the supplied file.
        """

        for loader in self._loaders:
            if loader.supports(file_path):
                return loader

        raise UnsupportedLoaderError(f"No loader registered for '{file_path.suffix}'.")
