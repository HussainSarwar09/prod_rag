"""
PDF loader.
"""

from pathlib import Path

from app.loaders.base import BaseDocumentLoader
from app.readers.pdf_reader import PDFReader
from app.services.metadata.extractor import MetadataExtractor


class PDFLoader(BaseDocumentLoader):
    def __init__(
        self,
        reader: PDFReader,
        metadata_extractor: MetadataExtractor,
    ) -> None:

        super().__init__(metadata_extractor)

        self._reader = reader

    def supports(self, file_path: Path) -> bool:
        return file_path.suffix.lower() == ".pdf"

    def read_content(self, file_path: Path) -> str:
        return self._reader.read(file_path)
