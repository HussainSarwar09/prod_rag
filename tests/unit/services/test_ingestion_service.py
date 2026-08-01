from pathlib import Path

from app.chunking import DocumentChunker
from app.config.chunking import ChunkingSettings
from app.config.embedding import EmbeddingSettings
from app.core.providers.embeddings.mock import MockEmbeddingProvider
from app.domain.document import Document
from app.domain.document_metadata import DocumentMetadata
from app.loaders.factory import LoaderFactory
from app.services.ingestion.service import IngestionService


def test_ingestion_service_embeds_chunked_documents() -> None:
    service = IngestionService(
        loader_factory=LoaderFactory(loaders=[_DocumentLoaderStub()]),
        chunker=DocumentChunker(
            ChunkingSettings(
                default_strategy="token_window",
                file_type_policies={},
            )
        ),
        embedding_model=MockEmbeddingProvider(EmbeddingSettings(provider="mock").mock),
    )

    result = service.ingest_path(Path("sample.txt"))

    assert result.chunk_count == 1
    assert result.chunks[0].embedding is not None
    assert len(result.chunks[0].embedding or []) == 8


class _DocumentLoaderStub:
    def supports(self, path: Path) -> bool:
        return path.suffix == ".txt"

    def load(self, path: Path) -> Document:
        content = "alpha beta gamma"
        return Document(
            content=content,
            metadata=DocumentMetadata(
                filename=path.name,
                extension=path.suffix,
                mime_type="text/plain",
                file_size=len(content),
                checksum="stub-checksum",
            ),
        )
