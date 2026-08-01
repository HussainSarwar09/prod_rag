import os

import httpx
import pytest

from app.config.embedding import EmbeddingSettings
from app.core.providers.embeddings import (
    BGEEmbeddingProvider,
    MockEmbeddingProvider,
    OpenAIEmbeddingProvider,
    build_embedding_provider,
)
from app.core.providers.embeddings.preprocessing import EmbeddingPreprocessor


def test_build_embedding_provider_uses_mock_provider() -> None:
    provider = build_embedding_provider(EmbeddingSettings(provider="mock"))

    assert isinstance(provider, MockEmbeddingProvider)


def test_build_embedding_provider_uses_bge_provider_with_injected_encoder() -> None:
    settings = EmbeddingSettings(provider="bge")
    provider = BGEEmbeddingProvider(settings.bge, encoder=_FakeEncoder())

    vectors = provider.embed_documents(["hello world"])

    assert vectors == [[0.1, 0.2, 0.3]]


def test_preprocessor_batches_and_truncates_inputs() -> None:
    preprocessor = EmbeddingPreprocessor(
        tokenizer_name="definitely-not-real",
        max_input_tokens=3,
        truncate=True,
        batch_size=2,
        max_batch_tokens=4,
    )

    batches = preprocessor.batch(
        [
            "one two three four",
            "alpha beta",
            "cat dog eel fox",
        ]
    )

    assert len(batches) == 3
    assert batches[0][0].truncated is True
    assert batches[0][0].token_count == 3


def test_preprocessor_rejects_oversized_input_without_truncation() -> None:
    preprocessor = EmbeddingPreprocessor(
        tokenizer_name="definitely-not-real",
        max_input_tokens=2,
        truncate=False,
        batch_size=2,
        max_batch_tokens=4,
    )

    with pytest.raises(ValueError, match="exceeds"):
        preprocessor.prepare("one two three")


def test_openai_provider_requires_api_key() -> None:
    settings = EmbeddingSettings(provider="openai")
    original = os.environ.pop(settings.openai.api_key_env, None)

    try:
        with pytest.raises(RuntimeError, match=settings.openai.api_key_env):
            OpenAIEmbeddingProvider(settings.openai)
    finally:
        if original is not None:
            os.environ[settings.openai.api_key_env] = original


def test_openai_provider_batches_requests() -> None:
    settings = EmbeddingSettings(provider="openai")
    settings.openai.batch_size = 2
    settings.openai.max_input_tokens = 20
    settings.openai.max_batch_tokens = 3
    settings.openai.tokenizer_name = "definitely-not-real"
    os.environ[settings.openai.api_key_env] = "test-key"
    client = _FakeOpenAIClient()
    provider = OpenAIEmbeddingProvider(settings.openai, client=client)

    vectors = provider.embed_documents(["one two", "three four", "five six"])

    assert len(vectors) == 3
    assert client.calls == 3


class _FakeEncoder:
    def encode(self, texts: list[str], **_: object) -> list[list[float]]:
        return [[0.1, 0.2, 0.3] for _ in texts]


class _FakeOpenAIClient:
    def __init__(self) -> None:
        self.calls = 0

    def post(self, _: str, json: dict[str, object]) -> httpx.Response:
        self.calls += 1
        inputs = json["input"]
        assert isinstance(inputs, list)
        data = [{"embedding": [0.1, 0.2, 0.3]} for _ in inputs]
        request = httpx.Request("POST", "https://example.test/embeddings")
        return httpx.Response(status_code=200, json={"data": data}, request=request)
