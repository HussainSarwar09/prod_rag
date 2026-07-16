"""
Shared implementation for text-based loaders.
"""

from abc import abstractmethod
from pathlib import Path

from app.loaders.base import BaseDocumentLoader
from app.readers.text_reader import TextReader
from app.services.metadata.extractor import MetadataExtractor


class BaseTextLoader(BaseDocumentLoader):
    def __init__(
        self,
        reader: TextReader,
        metadata: MetadataExtractor,
    ) -> None:

        super().__init__(metadata)

        self._reader = reader

    @property
    @abstractmethod
    def supported_extensions(self) -> tuple[str, ...]: ...

    def supports(self, file_path: Path) -> bool:
        return file_path.suffix.lower() in self.supported_extensions

    def read_content(self, file_path: Path) -> str:
        return self._reader.read(file_path)
