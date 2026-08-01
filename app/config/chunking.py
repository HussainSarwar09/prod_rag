from pydantic import BaseModel, Field


class ChunkingSettings(BaseModel):
    """Settings for deterministic, embedding-ready document chunks."""

    chunk_size_tokens: int = Field(default=384, ge=1)
    chunk_overlap_tokens: int = Field(default=48, ge=0)
    version: str = "token-window-v1"
