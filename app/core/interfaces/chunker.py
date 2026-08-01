"""
Document chunker interface.
"""

from typing import Protocol

from app.domain.chunk import Chunk
from app.domain.document import Document


class DocumentChunkerProtocol(Protocol):
    """
    Contract implemented by document chunking services.
    """

    def chunk(self, document: Document) -> list[Chunk]:
        """
        Split a normalized document into retrieval-ready chunks.
        """
        ...
