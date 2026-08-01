"""Ingestion service orchestrating load -> chunk -> embed."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from app.core.interfaces.chunker import DocumentChunkerProtocol
from app.core.interfaces.embedding import EmbeddingModel
from app.domain.chunk import Chunk
from app.domain.document import Document
from app.loaders.factory import LoaderFactory


@dataclass(slots=True)
class IngestionResult:
    document: Document
    chunks: list[Chunk]

    @property
    def chunk_count(self) -> int:
        return len(self.chunks)


class IngestionService:
    """Run the ingestion pipeline up to embedding generation."""

    def __init__(
        self,
        loader_factory: LoaderFactory,
        chunker: DocumentChunkerProtocol,
        embedding_model: EmbeddingModel,
    ) -> None:
        self._loader_factory = loader_factory
        self._chunker = chunker
        self._embedding_model = embedding_model

    def ingest_path(self, path: Path) -> IngestionResult:
        loader = self._loader_factory.get_loader(path)
        document = loader.load(path)
        return self.ingest_document(document)

    def ingest_document(self, document: Document) -> IngestionResult:
        chunks = self._chunker.chunk(document)
        embeddings = self._embedding_model.embed_documents([chunk.content for chunk in chunks])
        for chunk, embedding in zip(chunks, embeddings, strict=True):
            chunk.embedding = embedding
        return IngestionResult(document=document, chunks=chunks)
