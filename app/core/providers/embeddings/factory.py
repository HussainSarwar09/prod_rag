"""Embedding provider factory."""

from __future__ import annotations

from app.config.embedding import EmbeddingSettings
from app.core.interfaces.embedding import EmbeddingModel
from app.core.providers.embeddings.bge import BGEEmbeddingProvider
from app.core.providers.embeddings.mock import MockEmbeddingProvider
from app.core.providers.embeddings.openai import OpenAIEmbeddingProvider


def build_embedding_provider(settings: EmbeddingSettings) -> EmbeddingModel:
    if settings.provider == "bge":
        return BGEEmbeddingProvider(settings.bge)
    if settings.provider == "openai":
        return OpenAIEmbeddingProvider(settings.openai)
    if settings.provider == "mock":
        return MockEmbeddingProvider(settings.mock)
    raise ValueError(f"Unsupported embedding provider: {settings.provider}")
