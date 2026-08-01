"""Remote OpenAI embedding provider."""

from __future__ import annotations

import os
from time import sleep
from typing import Any

import httpx

from app.config.embedding import OpenAIProviderSettings
from app.core.interfaces.embedding import EmbeddingModel
from app.core.providers.embeddings.preprocessing import EmbeddingPreprocessor


class OpenAIEmbeddingProvider(EmbeddingModel):
    """HTTP client wrapper for OpenAI embeddings."""

    def __init__(
        self,
        settings: OpenAIProviderSettings,
        client: httpx.Client | None = None,
    ) -> None:
        self._settings = settings
        self._api_key = os.getenv(settings.api_key_env)
        if not self._api_key:
            raise RuntimeError(
                f"OpenAI embeddings require the environment variable {settings.api_key_env}."
            )
        self._client = client or httpx.Client(
            base_url=settings.api_base.rstrip("/"),
            timeout=settings.timeout_seconds,
            headers={
                "Authorization": f"Bearer {self._api_key}",
                "Content-Type": "application/json",
            },
        )
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
        vectors: list[list[float]] = []
        for batch in self._preprocessor.batch(texts):
            vectors.extend(self._request_embeddings([item.text for item in batch]))
        return vectors

    def embed_query(self, text: str) -> list[float]:
        return self._request_embeddings([self._preprocessor.prepare(text).text])[0]

    def _request_embeddings(self, inputs: list[str]) -> list[list[float]]:
        payload: dict[str, Any] = {
            "model": self._settings.model,
            "input": inputs,
        }
        if self._settings.dimensions is not None:
            payload["dimensions"] = self._settings.dimensions

        last_error: Exception | None = None
        for attempt in range(self._settings.retry_attempts + 1):
            try:
                response = self._client.post("/embeddings", json=payload)
                response.raise_for_status()
                data = response.json()["data"]
                return [list(map(float, item["embedding"])) for item in data]
            except httpx.HTTPError as exc:
                last_error = exc
                if attempt < self._settings.retry_attempts:
                    sleep(self._settings.retry_backoff_seconds * (2**attempt))
        raise RuntimeError("OpenAI embedding request failed after retries.") from last_error


__all__ = ["OpenAIEmbeddingProvider"]
