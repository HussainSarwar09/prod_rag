"""
Document loader interface.
"""

from pathlib import Path
from typing import Protocol

from app.domain.document import Document


class DocumentLoader(Protocol):
    """
    Contract implemented by all document loaders.
    """

    def supports(self, file_path: Path) -> bool:
        """
        Return True if this loader supports the supplied file.
        """
        ...

    def load(self, file_path: Path) -> Document:
        """
        Load a document into the common domain model.
        """
        ...
