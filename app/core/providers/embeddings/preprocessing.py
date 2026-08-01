"""Shared preprocessing for production-style embedding providers."""

from __future__ import annotations

from dataclasses import dataclass
from re import findall
from typing import Protocol, cast


class Tokenizer(Protocol):
    def encode(self, text: str) -> list[int]: ...

    def decode(self, tokens: list[int]) -> str: ...


class _WhitespaceTokenizer:
    def encode(self, text: str) -> list[int]:
        return list(range(len(findall(r"\S+", text))))

    def decode(self, tokens: list[int]) -> str:
        return " ".join(f"tok{i}" for i in tokens)


def build_tokenizer(tokenizer_name: str) -> Tokenizer:
    try:
        import tiktoken
    except ImportError:
        return _WhitespaceTokenizer()

    try:
        return cast(Tokenizer, tiktoken.get_encoding(tokenizer_name))
    except ValueError:
        return _WhitespaceTokenizer()


@dataclass(frozen=True, slots=True)
class PreparedText:
    text: str
    token_count: int
    truncated: bool


class EmbeddingPreprocessor:
    """Applies token budgeting, truncation, and batch planning."""

    def __init__(
        self,
        *,
        tokenizer_name: str,
        max_input_tokens: int,
        truncate: bool,
        batch_size: int,
        max_batch_tokens: int,
    ) -> None:
        self._tokenizer = build_tokenizer(tokenizer_name)
        self._max_input_tokens = max_input_tokens
        self._truncate = truncate
        self._batch_size = batch_size
        self._max_batch_tokens = max_batch_tokens

    def prepare(self, text: str) -> PreparedText:
        tokens = self._tokenizer.encode(text)
        token_count = len(tokens)
        if token_count <= self._max_input_tokens:
            return PreparedText(text=text, token_count=token_count, truncated=False)
        if not self._truncate:
            raise ValueError(
                f"Embedding input exceeds max_input_tokens={self._max_input_tokens} "
                f"with token_count={token_count}."
            )
        truncated_tokens = tokens[: self._max_input_tokens]
        truncated_text = self._tokenizer.decode(truncated_tokens)
        return PreparedText(
            text=truncated_text,
            token_count=len(truncated_tokens),
            truncated=True,
        )

    def batch(self, texts: list[str]) -> list[list[PreparedText]]:
        prepared = [self.prepare(text) for text in texts]
        batches: list[list[PreparedText]] = []
        current: list[PreparedText] = []
        current_tokens = 0
        for item in prepared:
            would_exceed_size = len(current) >= self._batch_size
            would_exceed_tokens = current_tokens + item.token_count > self._max_batch_tokens
            if current and (would_exceed_size or would_exceed_tokens):
                batches.append(current)
                current = []
                current_tokens = 0
            current.append(item)
            current_tokens += item.token_count
        if current:
            batches.append(current)
        return batches
