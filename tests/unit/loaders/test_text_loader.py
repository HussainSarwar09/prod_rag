from pathlib import Path

from app.loaders.text_loader import TextLoader
from app.readers.text_reader import TextReader
from app.services.metadata.extractor import MetadataExtractor


def test_text_loader(
    text_reader: TextReader,
    metadata_extractor: MetadataExtractor,
) -> None:
    loader = TextLoader(
        reader=text_reader,
        metadata_extractor=metadata_extractor,
    )

    assert loader.supports(Path("document.txt"))
    assert not loader.supports(Path("document.pdf"))
    assert not loader.supports(Path("document.md"))
