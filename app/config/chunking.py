from typing import Literal

from pydantic import BaseModel, Field

StrategyType = Literal["auto", "token_window", "sentence", "paragraph", "markdown", "json", "code"]


class _BaseStrategySettings(BaseModel):
    chunk_size_tokens: int = Field(default=384, ge=1)
    chunk_overlap_tokens: int = Field(default=48, ge=0)
    version_suffix: str = "v1"


class TokenWindowChunkingStrategySettings(_BaseStrategySettings):
    pass


class SentenceChunkingStrategySettings(_BaseStrategySettings):
    chunk_size_tokens: int = Field(default=320, ge=1)
    chunk_overlap_tokens: int = Field(default=40, ge=0)
    max_sentences_per_chunk: int = Field(default=12, ge=1)


class ParagraphChunkingStrategySettings(_BaseStrategySettings):
    chunk_size_tokens: int = Field(default=420, ge=1)
    chunk_overlap_tokens: int = Field(default=60, ge=0)
    max_paragraphs_per_chunk: int = Field(default=6, ge=1)


class MarkdownChunkingStrategySettings(_BaseStrategySettings):
    chunk_size_tokens: int = Field(default=320, ge=1)
    chunk_overlap_tokens: int = Field(default=32, ge=0)


class JsonChunkingStrategySettings(_BaseStrategySettings):
    chunk_size_tokens: int = Field(default=256, ge=1)
    chunk_overlap_tokens: int = Field(default=24, ge=0)


class CodeChunkingStrategySettings(_BaseStrategySettings):
    chunk_size_tokens: int = Field(default=240, ge=1)
    chunk_overlap_tokens: int = Field(default=32, ge=0)


ChunkingStrategySettings = (
    TokenWindowChunkingStrategySettings
    | SentenceChunkingStrategySettings
    | ParagraphChunkingStrategySettings
    | MarkdownChunkingStrategySettings
    | JsonChunkingStrategySettings
    | CodeChunkingStrategySettings
)


class FileTypeChunkingPolicy(BaseModel):
    strategy: StrategyType = "auto"


def _default_file_type_policies() -> dict[str, FileTypeChunkingPolicy]:
    return {
        ".md": FileTypeChunkingPolicy(strategy="markdown"),
        ".markdown": FileTypeChunkingPolicy(strategy="markdown"),
        ".txt": FileTypeChunkingPolicy(strategy="paragraph"),
        ".rst": FileTypeChunkingPolicy(strategy="paragraph"),
        ".pdf": FileTypeChunkingPolicy(strategy="sentence"),
        "application/pdf": FileTypeChunkingPolicy(strategy="sentence"),
        ".json": FileTypeChunkingPolicy(strategy="json"),
        ".jsonl": FileTypeChunkingPolicy(strategy="json"),
        "application/json": FileTypeChunkingPolicy(strategy="json"),
        ".py": FileTypeChunkingPolicy(strategy="code"),
        ".js": FileTypeChunkingPolicy(strategy="code"),
        ".ts": FileTypeChunkingPolicy(strategy="code"),
        ".tsx": FileTypeChunkingPolicy(strategy="code"),
        ".jsx": FileTypeChunkingPolicy(strategy="code"),
        ".java": FileTypeChunkingPolicy(strategy="code"),
        ".go": FileTypeChunkingPolicy(strategy="code"),
    }


class ChunkingSettings(BaseModel):
    """Enterprise-style chunking policies and strategy settings."""

    version: str = "enterprise-chunking-v1"
    default_strategy: StrategyType = "auto"
    token_window: TokenWindowChunkingStrategySettings = TokenWindowChunkingStrategySettings()
    sentence: SentenceChunkingStrategySettings = SentenceChunkingStrategySettings()
    paragraph: ParagraphChunkingStrategySettings = ParagraphChunkingStrategySettings()
    markdown: MarkdownChunkingStrategySettings = MarkdownChunkingStrategySettings()
    json_strategy: JsonChunkingStrategySettings = JsonChunkingStrategySettings()
    code: CodeChunkingStrategySettings = CodeChunkingStrategySettings()
    file_type_policies: dict[str, FileTypeChunkingPolicy] = Field(
        default_factory=_default_file_type_policies
    )
