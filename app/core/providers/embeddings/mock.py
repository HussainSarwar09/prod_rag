"""Deterministic mock embedding provider for tests and local development."""

from __future__ import annotations

from hashlib import sha256

from app.config.embedding import MockProviderSettings
from app.core.interfaces.embedding import EmbeddingModel


class MockEmbeddingProvider(EmbeddingModel):
    def __init__(self, settings: MockProviderSettings) -> None:
        self._settings = settings

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [self._embed(text) for text in texts]

    def embed_query(self, text: str) -> list[float]:
        return self._embed(text)

    def _embed(self, text: str) -> list[float]:
        digest = sha256(text.encode("utf-8")).digest()
        values = []
        for index in range(self._settings.dimensions):
            byte = digest[index % len(digest)]
            values.append(round(byte / 255.0, 6))
        return values


__all__ = ["MockEmbeddingProvider"]
