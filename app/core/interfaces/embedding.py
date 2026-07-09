from typing import Protocol


class EmbeddingModel(Protocol):
    """
    Contract for embedding providers.
    """

    def embed_documents(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        ...

    def embed_query(
        self,
        text: str,
    ) -> list[float]:
        ...