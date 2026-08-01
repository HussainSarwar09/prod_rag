from dataclasses import dataclass, field

from app.domain.base import BaseEntity
from app.domain.chunk_metadata import ChunkMetadata


@dataclass(slots=True)
class Chunk(BaseEntity):
    """Represents a chunk of a document."""

    document_id: str = ""
    content: str = ""
    index: int = 0
    token_count: int = 0
    start_offset: int = 0
    end_offset: int = 0
    metadata: ChunkMetadata = field(default_factory=ChunkMetadata)
    previous_chunk_id: str | None = None
    next_chunk_id: str | None = None

    def __post_init__(self) -> None:
        """Validate invariants required for reliable source citations."""
        if not self.content.strip():
            raise ValueError("Chunk content must not be empty or whitespace-only.")
        if self.index < 0:
            raise ValueError("Chunk index must not be negative.")
        if self.token_count < 0:
            raise ValueError("Chunk token_count must not be negative.")
        if self.start_offset < 0:
            raise ValueError("Chunk start_offset must not be negative.")
        if self.end_offset < self.start_offset:
            raise ValueError("Chunk end_offset must not precede start_offset.")
        if self.end_offset - self.start_offset != len(self.content):
            raise ValueError("Chunk offsets must describe exactly the chunk content.")

    @property
    def character_count(self) -> int:
        """Return the number of characters in this chunk."""
        return len(self.content)
