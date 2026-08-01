"""
Application dependency container.

Responsible for creating and managing shared application services.
"""

from app.chunking.chunker import DocumentChunker
from app.config.settings import get_settings
from app.loaders.factory import LoaderFactory
from app.loaders.markdown_loader import MarkdownLoader
from app.loaders.pdf_loader import PDFLoader
from app.loaders.text_loader import TextLoader
from app.readers.pdf_reader import PDFReader
from app.readers.text_reader import TextReader
from app.services.metadata.extractor import MetadataExtractor


class Container:
    """Application service container."""

    def __init__(self) -> None:
        self.settings = get_settings()

        #
        # Shared services
        #
        self.metadata_extractor = MetadataExtractor()

        self.document_chunker = DocumentChunker(self.settings.chunking)

        #
        # Readers
        #
        self.text_reader = TextReader()
        self.pdf_reader = PDFReader()

        #
        # Loaders
        #
        self.text_loader = TextLoader(
            reader=self.text_reader,
            metadata_extractor=self.metadata_extractor,
        )

        self.markdown_loader = MarkdownLoader(
            reader=self.text_reader,
            metadata_extractor=self.metadata_extractor,
        )

        self.pdf_loader = PDFLoader(
            reader=self.pdf_reader,
            metadata_extractor=self.metadata_extractor,
        )

        #
        # Factories
        #
        self.loader_factory = LoaderFactory(
            loaders=[
                self.text_loader,
                self.markdown_loader,
                self.pdf_loader,
            ]
        )


container = Container()
