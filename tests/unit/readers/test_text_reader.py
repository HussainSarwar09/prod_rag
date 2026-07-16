"""
Unit tests for TextReader.
"""

from pathlib import Path

import pytest

from app.readers.text_reader import TextReader

FIXTURE_DIR = Path(__file__).resolve().parents[2] / "fixtures"


def test_read_text_file() -> None:
    """
    TextReader should read UTF-8 text files.
    """

    reader = TextReader()

    content = reader.read(FIXTURE_DIR / "sample.txt")

    assert "Hello Production RAG!" in content
    assert "Line 3." in content


def test_missing_file() -> None:
    """
    Reading a missing file should raise FileNotFoundError.
    """

    reader = TextReader()

    with pytest.raises(FileNotFoundError):
        reader.read(FIXTURE_DIR / "does_not_exist.txt")
