"""
Markdown loader.
"""

from app.loaders.base_text_loader import BaseTextLoader
from app.readers.text_reader import TextReader
from app.services.metadata.extractor import MetadataExtractor


class MarkdownLoader(BaseTextLoader):
    def __init__(
        self,
        reader: TextReader,
        metadata_extractor: MetadataExtractor,
    ) -> None:

        super().__init__(reader, metadata_extractor)

    @property
    def supported_extensions(self) -> tuple[str, ...]:
        return (
            ".md",
            ".markdown",
        )
