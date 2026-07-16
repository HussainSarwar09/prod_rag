from pathlib import Path

import pytest

from app.exceptions.document import (
    CorruptedDocumentError,
    DocumentNotFoundError,
)
from app.readers.pdf_reader import PDFReader

FIXTURE_DIR = Path(__file__).resolve().parents[2] / "fixtures" / "pdf"


def test_single_page_pdf() -> None:
    reader = PDFReader()

    text = reader.read(FIXTURE_DIR / "single_page.pdf")

    assert "This is page 1" in text


def test_multi_page_pdf() -> None:
    reader = PDFReader()

    text = reader.read(FIXTURE_DIR / "multi_page.pdf")

    assert "This is page 1" in text
    assert "This is page 2" in text
    assert "This is page 3" in text


def test_missing_pdf() -> None:
    reader = PDFReader()

    with pytest.raises(DocumentNotFoundError):
        reader.read(FIXTURE_DIR / "missing.pdf")


def test_corrupt_pdf() -> None:
    reader = PDFReader()

    with pytest.raises(CorruptedDocumentError):
        reader.read(FIXTURE_DIR / "corrupt.pdf")
