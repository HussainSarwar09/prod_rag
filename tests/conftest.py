from collections.abc import Generator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.readers.pdf_reader import PDFReader
from app.readers.text_reader import TextReader
from app.services.metadata.extractor import MetadataExtractor


@pytest.fixture
def client() -> Generator[TestClient]:
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def text_reader() -> TextReader:
    return TextReader()


@pytest.fixture
def pdf_reader() -> PDFReader:
    return PDFReader()


@pytest.fixture
def metadata_extractor() -> MetadataExtractor:
    return MetadataExtractor()


@pytest.fixture
def sample_text_file() -> Path:
    return Path(__file__).parent / "fixtures" / "sample.txt"


@pytest.fixture
def sample_pdf_file() -> Path:
    return Path(__file__).parent / "fixtures" / "pdf" / "single_page.pdf"
