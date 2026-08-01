import pytest

from app.chunking import DocumentChunker
from app.config.chunking import ChunkingSettings, FileTypeChunkingPolicy
from app.domain.document import Document
from app.domain.document_metadata import DocumentMetadata


def _document(content: str, extension: str = ".txt", mime_type: str | None = None) -> Document:
    return Document(
        content=content,
        metadata=DocumentMetadata(
            filename=f"sample{extension}",
            extension=extension,
            mime_type=mime_type or ("text/markdown" if extension == ".md" else "text/plain"),
            file_size=len(content),
            checksum="source-checksum",
        ),
    )


def test_markdown_strategy_is_selected_by_default_policy() -> None:
    document = _document("# Guide\nintro words\n## Install\ninstall words", ".md")
    chunker = DocumentChunker()

    assert chunker.resolve_strategy(document) == "markdown"

    chunks = chunker.chunk(document)
    assert chunks[1].metadata.heading_path == ("Guide", "Install")
    assert chunks[1].metadata.heading == "Install"
    assert chunks[1].metadata.chunking_strategy == "markdown"


def test_paragraph_strategy_is_selected_for_text_and_preserves_overlap_links() -> None:
    content = "alpha beta\n\ncharlie delta\n\necho foxtrot"
    document = _document(content, ".txt")
    settings = ChunkingSettings()
    settings.paragraph.chunk_size_tokens = 4
    settings.paragraph.chunk_overlap_tokens = 2
    settings.paragraph.max_paragraphs_per_chunk = 2
    chunker = DocumentChunker(settings)

    chunks = chunker.chunk(document)

    assert chunker.resolve_strategy(document) == "paragraph"
    assert len(chunks) == 2
    assert chunks[0].next_chunk_id == chunks[1].id
    assert chunks[1].previous_chunk_id == chunks[0].id
    assert all(
        chunk.content == document.content[chunk.start_offset : chunk.end_offset] for chunk in chunks
    )


def test_json_strategy_can_be_selected_and_produces_stable_ids() -> None:
    content = '{\n  "customer": {"name": "Ada"},\n  "invoice": {"total": 42}\n}'
    document = _document(content, ".json", "application/json")
    chunker = DocumentChunker()

    first_run = chunker.chunk(document)
    second_run = chunker.chunk(_document(content, ".json", "application/json"))

    assert chunker.resolve_strategy(document) == "json"
    assert [chunk.id for chunk in first_run] == [chunk.id for chunk in second_run]
    assert all(chunk.metadata.chunking_strategy == "json" for chunk in first_run)


def test_code_strategy_detects_code_files() -> None:
    document = _document(
        "import os\n\n\ndef build():\n    return 1\n\nclass Service:\n    pass\n",
        ".py",
        "text/x-python",
    )
    chunker = DocumentChunker()

    chunks = chunker.chunk(document)

    assert chunker.resolve_strategy(document) == "code"
    assert len(chunks) >= 2
    assert all(chunk.metadata.chunking_strategy == "code" for chunk in chunks)


def test_file_type_policy_can_override_auto_selection() -> None:
    settings = ChunkingSettings(
        file_type_policies={
            **ChunkingSettings().file_type_policies,
            ".txt": FileTypeChunkingPolicy(strategy="sentence"),
        }
    )
    document = _document("One. Two. Three.", ".txt")
    chunker = DocumentChunker(settings)

    assert chunker.resolve_strategy(document) == "sentence"
    assert all(chunk.metadata.chunking_strategy == "sentence" for chunk in chunker.chunk(document))


def test_auto_falls_back_to_token_window_for_unknown_file_types() -> None:
    settings = ChunkingSettings()
    settings.default_strategy = "auto"
    settings.token_window.chunk_size_tokens = 3
    settings.token_window.chunk_overlap_tokens = 1
    document = _document("one two three four five", ".bin", "application/octet-stream")
    chunker = DocumentChunker(settings)

    chunks = chunker.chunk(document)

    assert chunker.resolve_strategy(document) == "token_window"
    assert [chunk.content for chunk in chunks] == ["one two three", "three four five"]
    assert all(chunk.metadata.chunking_strategy == "token_window" for chunk in chunks)


def test_empty_document_produces_no_chunks() -> None:
    assert DocumentChunker().chunk(_document("  \n\t")) == []


def test_invalid_overlap_is_rejected() -> None:
    settings = ChunkingSettings()
    settings.token_window.chunk_size_tokens = 3
    settings.token_window.chunk_overlap_tokens = 3

    with pytest.raises(ValueError, match="smaller"):
        DocumentChunker(settings)
