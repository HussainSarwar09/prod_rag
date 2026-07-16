"""
Document domain entity.
"""

from dataclasses import dataclass

from app.domain.base import BaseEntity
from app.domain.document_metadata import DocumentMetadata
from app.enums.document import DocumentStatus


@dataclass(slots=True)
class Document(BaseEntity):
    """
    Represents a normalized source document.
    """

    content: str

    metadata: DocumentMetadata

    status: DocumentStatus = DocumentStatus.RECEIVED
