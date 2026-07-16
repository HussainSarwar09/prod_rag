"""
Base implementation for all document loaders.
"""

from abc import ABC, abstractmethod
from pathlib import Path

from app.domain.document import Document
from app.enums.document import DocumentStatus
from app.services.metadata.extractor import MetadataExtractor


class BaseDocumentLoader(ABC):
    """
    Base implementation for all document loaders.

    Implements the Template Method pattern by defining the common workflow
    for loading a document while delegating content extraction to subclasses.
    """

    def __init__(
        self,
        metadata_extractor: MetadataExtractor,
    ) -> None:
        self._metadata_extractor = metadata_extractor

    def load(self, file_path: Path) -> Document:
        """
        Load a file into the common Document domain model.
        """

        content = self.read_content(file_path)

        metadata = self._metadata_extractor.extract(file_path)

        return Document(
            content=content,
            metadata=metadata,
            status=DocumentStatus.LOADED,
        )

    @abstractmethod
    def supports(self, file_path: Path) -> bool:
        """
        Return True if this loader supports the supplied file.
        """
        ...

    @abstractmethod
    def read_content(self, file_path: Path) -> str:
        """
        Read the supplied file and return normalized text.
        """
        ...
