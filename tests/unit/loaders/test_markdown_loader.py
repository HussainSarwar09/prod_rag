from pathlib import Path

from app.loaders.markdown_loader import MarkdownLoader
from app.readers.text_reader import TextReader
from app.services.metadata.extractor import MetadataExtractor


def test_markdown_loader(
    text_reader: TextReader,
    metadata_extractor: MetadataExtractor,
) -> None:
    loader = MarkdownLoader(
        reader=text_reader,
        metadata_extractor=metadata_extractor,
    )

    assert loader.supports(Path("README.md"))
    assert loader.supports(Path("README.markdown"))
    assert not loader.supports(Path("README.txt"))
    assert not loader.supports(Path("README.pdf"))
