from pathlib import Path

import fitz

from app.exceptions.document import (
    CorruptedDocumentError,
    DocumentNotFoundError,
)
from app.readers.base import BaseReader


class PDFReader(BaseReader):
    def read(self, file_path: Path) -> str:

        if not file_path.exists():
            raise DocumentNotFoundError(str(file_path))

        try:
            text: list[str] = []

            with fitz.open(file_path) as pdf:
                for page in pdf:
                    page_text = page.get_text()

                    if page_text.strip():
                        text.append(page_text)

            return "\n".join(text)

        except fitz.FileDataError as exc:
            raise CorruptedDocumentError(f"Failed to read '{file_path.name}'.") from exc
