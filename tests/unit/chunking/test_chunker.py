import pytest

from app.chunking import DocumentChunker
from app.config.chunking import ChunkingSettings
from app.domain.document import Document
from app.domain.document_metadata import DocumentMetadata


def _document(content: str, extension: str = ".txt") -> Document:
    return Document(
        content=content,
        metadata=DocumentMetadata(
            filename=f"sample{extension}",
            extension=extension,
            mime_type="text/markdown" if extension == ".md" else "text/plain",
            file_size=len(content),
            checksum="source-checksum",
        ),
    )


def test_chunks_preserve_source_spans_and_overlap() -> None:
    document = _document("one two three four five six seven")
    chunks = DocumentChunker(ChunkingSettings(chunk_size_tokens=3, chunk_overlap_tokens=1)).chunk(
        document
    )

    assert [chunk.content for chunk in chunks] == [
        "one two three",
        "three four five",
        "five six seven",
    ]
    assert all(
        chunk.content == document.content[chunk.start_offset : chunk.end_offset]
        for chunk in chunks
    )
    assert chunks[0].next_chunk_id == chunks[1].id
    assert chunks[1].previous_chunk_id == chunks[0].id


def test_markdown_chunk_has_heading_provenance_and_stable_id() -> None:
    document = _document("# Guide\nintro words\n## Install\ninstall words", ".md")
    reloaded_document = _document("# Guide\nintro words\n## Install\ninstall words", ".md")
    chunker = DocumentChunker(ChunkingSettings(chunk_size_tokens=20, chunk_overlap_tokens=0))

    first_run = chunker.chunk(document)
    second_run = chunker.chunk(reloaded_document)

    assert [chunk.id for chunk in first_run] == [chunk.id for chunk in second_run]
    assert first_run[1].metadata.heading_path == ("Guide", "Install")
    assert first_run[1].metadata.heading == "Install"


def test_markdown_preamble_is_not_discarded() -> None:
    document = _document("Preamble text\n# Guide\nBody text", ".md")
    chunks = DocumentChunker(ChunkingSettings(chunk_size_tokens=20, chunk_overlap_tokens=0)).chunk(
        document
    )

    assert [chunk.content for chunk in chunks] == ["Preamble text", "# Guide\nBody text"]
    assert chunks[0].metadata.heading is None
    assert chunks[1].metadata.heading == "Guide"


def test_empty_document_produces_no_chunks() -> None:
    assert DocumentChunker().chunk(_document("  \n\t")) == []


def test_invalid_overlap_is_rejected() -> None:
    with pytest.raises(ValueError, match="smaller"):
        DocumentChunker(ChunkingSettings(chunk_size_tokens=3, chunk_overlap_tokens=3))
