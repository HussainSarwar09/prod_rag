"""
Chunk metadata domain model.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class ChunkMetadata:
    """
    Metadata associated with a document chunk.

    This information is propagated from the source document and enriched
    during chunk creation. It provides contextual information used for
    retrieval, citations, debugging, and future retrieval strategies.
    """

    page_number: int | None = None
    end_page_number: int | None = None
    section: str | None = None
    heading: str | None = None
    heading_path: tuple[str, ...] = ()
    language: str | None = None
    source_path: str = ""
    mime_type: str = ""
    content_hash: str = ""
    chunker_version: str = ""
    chunking_strategy: str = ""
