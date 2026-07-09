from typing import Protocol

from app.domain.answer import Answer
from app.domain.chunk import Chunk
from app.domain.query import Query


class LLM(Protocol):
    """
    Contract for language model providers.
    """

    async def generate(
        self,
        query: Query,
        context: list[Chunk],
    ) -> Answer:
        ...