"""Local-first BGE embedding provider."""

from __future__ import annotations

from typing import Any

from app.config.embedding import BGEProviderSettings
from app.core.interfaces.embedding import EmbeddingModel
from app.core.providers.embeddings.preprocessing import EmbeddingPreprocessor


class BGEEmbeddingProvider(EmbeddingModel):
    """Embed text locally with sentence-transformers-compatible BGE models."""

    def __init__(
        self,
        settings: BGEProviderSettings,
        encoder: Any | None = None,
    ) -> None:
        self._settings = settings
        self._encoder = encoder
        self._preprocessor = EmbeddingPreprocessor(
            tokenizer_name=settings.tokenizer_name,
            max_input_tokens=settings.max_input_tokens,
            truncate=settings.truncate,
            batch_size=settings.batch_size,
            max_batch_tokens=settings.max_batch_tokens,
        )

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        batches = self._preprocessor.batch([self._prepare_document(text) for text in texts])
        vectors: list[list[float]] = []
        for batch in batches:
            vectors.extend(self._encode([item.text for item in batch]))
        return vectors

    def embed_query(self, text: str) -> list[float]:
        prepared = self._prepare_query(text)
        return self._encode([self._preprocessor.prepare(prepared).text])[0]

    def _prepare_document(self, text: str) -> str:
        return f"{self._settings.document_instruction} {text}".strip()

    def _prepare_query(self, text: str) -> str:
        return f"{self._settings.query_instruction} {text}".strip()

    def _encode(self, texts: list[str]) -> list[list[float]]:
        if self._encoder is None:
            self._encoder = self._build_encoder()
        vectors = self._encoder.encode(
            texts,
            batch_size=self._settings.batch_size,
            normalize_embeddings=self._settings.normalize,
            show_progress_bar=False,
        )
        return [list(map(float, vector)) for vector in vectors]

    def _build_encoder(self) -> Any:
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError as exc:
            raise RuntimeError(
                "BGE embeddings require 'sentence-transformers'. Install it to run the local "
                "embedding pipeline."
            ) from exc
        return SentenceTransformer(self._settings.model, device=self._settings.device)


__all__ = ["BGEEmbeddingProvider"]
