from dataclasses import dataclass

from app.domain.base import BaseEntity


@dataclass(slots=True)
class Chunk(BaseEntity):
    """Represents a chunk of a document."""

    document_id: str = ""
    content: str = ""
