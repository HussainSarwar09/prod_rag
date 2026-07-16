from pathlib import Path

from app.services.metadata.extractor import MetadataExtractor


def test_metadata_extractor(
    metadata_extractor: MetadataExtractor,
    sample_text_file: Path,
) -> None:
    metadata = metadata_extractor.extract(sample_text_file)

    assert metadata.filename == "sample.txt"
