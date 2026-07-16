"""
Metadata extraction services.
"""

from pathlib import Path

from app.domain.document_metadata import DocumentMetadata
from app.utils.hashing import sha256_file


class MetadataExtractor:
    """
    Extracts metadata from documents.
    """

    MIME_TYPES = {
        ".txt": "text/plain",
        ".md": "text/markdown",
        ".markdown": "text/markdown",
        ".pdf": "application/pdf",
    }

    def extract(self, file_path: Path) -> DocumentMetadata:

        extension = file_path.suffix.lower()

        return DocumentMetadata(
            filename=file_path.name,
            extension=extension,
            mime_type=self.MIME_TYPES.get(
                extension,
                "application/octet-stream",
            ),
            file_size=file_path.stat().st_size,
            checksum=sha256_file(file_path),
        )
