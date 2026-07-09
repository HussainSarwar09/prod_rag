from typing import Protocol

from app.domain.chunk import Chunk
from app.domain.query import Query


class VectorStore(Protocol):
    """
    Contract that every vector database implementation
    must satisfy.
    """

    def add_chunks(self, chunks: list[Chunk]) -> None:
        """Store chunks in the vector database."""
        ...

    def similarity_search(
        self,
        query: Query,
        top_k: int = 5,
    ) -> list[Chunk]:
        """Return the most relevant chunks."""
        ...