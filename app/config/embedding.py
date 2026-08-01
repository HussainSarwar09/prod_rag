from typing import Literal

from pydantic import BaseModel, Field, model_validator

EmbeddingProviderType = Literal["bge", "openai", "mock"]


class BGEProviderSettings(BaseModel):
    model: str = "BAAI/bge-m3"
    device: str = "cpu"
    normalize: bool = True
    batch_size: int = Field(default=16, ge=1)
    max_batch_tokens: int = Field(default=16384, ge=1)
    max_input_tokens: int = Field(default=8192, ge=1)
    tokenizer_name: str = "cl100k_base"
    truncate: bool = True
    query_instruction: str = "Represent this query for retrieval:"
    document_instruction: str = "Represent this document for retrieval:"

    @model_validator(mode="after")
    def validate_batch_limits(self) -> "BGEProviderSettings":
        if self.max_batch_tokens < self.max_input_tokens:
            raise ValueError("max_batch_tokens must be >= max_input_tokens.")
        return self


class OpenAIProviderSettings(BaseModel):
    model: str = "text-embedding-3-large"
    dimensions: int | None = Field(default=None, ge=1)
    api_base: str = "https://api.openai.com/v1"
    api_key_env: str = "OPENAI_API_KEY"
    batch_size: int = Field(default=32, ge=1)
    max_batch_tokens: int = Field(default=32768, ge=1)
    max_input_tokens: int = Field(default=8192, ge=1)
    tokenizer_name: str = "cl100k_base"
    truncate: bool = True
    timeout_seconds: float = Field(default=30.0, gt=0.0)
    retry_attempts: int = Field(default=3, ge=0)
    retry_backoff_seconds: float = Field(default=1.0, ge=0.0)

    @model_validator(mode="after")
    def validate_batch_limits(self) -> "OpenAIProviderSettings":
        if self.max_batch_tokens < self.max_input_tokens:
            raise ValueError("max_batch_tokens must be >= max_input_tokens.")
        return self


class MockProviderSettings(BaseModel):
    dimensions: int = Field(default=8, ge=1)


class EmbeddingSettings(BaseModel):
    """Provider-aware settings for production-style embedding pipelines."""

    provider: EmbeddingProviderType = "bge"
    cache_enabled: bool = False
    cache_directory: str = "./data/embeddings-cache"
    bge: BGEProviderSettings = BGEProviderSettings()
    openai: OpenAIProviderSettings = OpenAIProviderSettings()
    mock: MockProviderSettings = MockProviderSettings()
