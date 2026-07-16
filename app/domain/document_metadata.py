"""
Document metadata value object.
"""

from dataclasses import dataclass, field


@dataclass(slots=True)
class DocumentMetadata:
    """
    Metadata describing a source document.
    """

    filename: str

    extension: str

    mime_type: str

    file_size: int

    checksum: str

    page_count: int = 0

    attributes: dict[str, str] = field(default_factory=dict)
