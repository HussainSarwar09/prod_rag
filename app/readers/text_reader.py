"""
UTF-8 text reader.
"""

from pathlib import Path

from app.readers.base import BaseReader


class TextReader(BaseReader):
    def read(self, file_path: Path) -> str:
        return file_path.read_text(
            encoding="utf-8",
            errors="replace",
        )
