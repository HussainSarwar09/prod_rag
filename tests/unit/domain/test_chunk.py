"""
Unit tests for the Chunk domain model.
"""

from uuid import uuid4

import pytest

from app.domain.chunk import Chunk


def test_chunk_creation() -> None:
    """
    A valid chunk should be created successfully.
    """
    chunk = Chunk(
        document_id=uuid4(),
        content="Hello production RAG",
        index=0,
        start_offset=0,
        end_offset=20,
    )

    assert chunk.content == "Hello production RAG"
    assert chunk.index == 0
    assert chunk.character_count == len("Hello production RAG")


def test_character_count_is_calculated() -> None:
    """
    Character count should be derived automatically.
    """
    chunk = Chunk(
        document_id=uuid4(),
        content="ABCDE",
        index=0,
        start_offset=0,
        end_offset=5,
    )

    assert chunk.character_count == 5


def test_chunk_can_store_embedding_vector() -> None:
    chunk = Chunk(
        document_id=str(uuid4()),
        content="ABCDE",
        index=0,
        start_offset=0,
        end_offset=5,
        embedding=[0.1, 0.2, 0.3],
    )

    assert chunk.embedding == [0.1, 0.2, 0.3]


def test_empty_content_raises_error() -> None:
    """
    Empty content is not allowed.
    """
    with pytest.raises(ValueError):
        Chunk(
            document_id=uuid4(),
            content="",
            index=0,
            start_offset=0,
            end_offset=0,
        )


def test_whitespace_content_raises_error() -> None:
    """
    Whitespace-only content is not allowed.
    """
    with pytest.raises(ValueError):
        Chunk(
            document_id=uuid4(),
            content="     ",
            index=0,
            start_offset=0,
            end_offset=5,
        )


def test_negative_index_raises_error() -> None:
    """
    Chunk index cannot be negative.
    """
    with pytest.raises(ValueError):
        Chunk(
            document_id=uuid4(),
            content="Hello",
            index=-1,
            start_offset=0,
            end_offset=5,
        )


def test_negative_start_offset_raises_error() -> None:
    """
    Start offset cannot be negative.
    """
    with pytest.raises(ValueError):
        Chunk(
            document_id=uuid4(),
            content="Hello",
            index=0,
            start_offset=-1,
            end_offset=5,
        )


def test_invalid_offsets_raise_error() -> None:
    """
    End offset must not precede start offset.
    """
    with pytest.raises(ValueError):
        Chunk(
            document_id=uuid4(),
            content="Hello",
            index=0,
            start_offset=10,
            end_offset=5,
        )


def test_offsets_must_match_content_length() -> None:
    with pytest.raises(ValueError, match="describe exactly"):
        Chunk(
            document_id=str(uuid4()),
            content="Hello",
            index=0,
            start_offset=0,
            end_offset=0,
        )


def test_empty_embedding_vector_is_rejected() -> None:
    with pytest.raises(ValueError, match="embedding"):
        Chunk(
            document_id=str(uuid4()),
            content="Hello",
            index=0,
            start_offset=0,
            end_offset=5,
            embedding=[],
        )
