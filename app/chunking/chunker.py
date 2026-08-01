"""Deterministic, source-span-preserving document chunking."""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from re import MULTILINE, Match, compile, finditer
from uuid import NAMESPACE_URL, uuid5

from app.config.chunking import ChunkingSettings
from app.domain.chunk import Chunk
from app.domain.chunk_metadata import ChunkMetadata
from app.domain.document import Document

TOKEN_PATTERN = compile(r"\S+")
MARKDOWN_HEADING_PATTERN = compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$", MULTILINE)


@dataclass(frozen=True, slots=True)
class _Section:
    start: int
    end: int
    heading_path: tuple[str, ...]


class DocumentChunker:
    """Split documents on token windows while preserving source offsets.

    Tokens are whitespace-delimited as a dependency-free baseline. Replace
    ``TOKEN_PATTERN`` with the embedding provider's tokenizer before relying
    on token limits enforced by a specific model.
    """

    def __init__(self, settings: ChunkingSettings | None = None) -> None:
        self._settings = settings or ChunkingSettings()
        if self._settings.chunk_overlap_tokens >= self._settings.chunk_size_tokens:
            raise ValueError("chunk_overlap_tokens must be smaller than chunk_size_tokens.")

    def chunk(self, document: Document) -> list[Chunk]:
        sections = self._sections(document.content, document.metadata.extension)
        drafts: list[tuple[int, int, int, tuple[str, ...]]] = []
        for section in sections:
            tokens = list(finditer(TOKEN_PATTERN, document.content[section.start : section.end]))
            if not tokens:
                continue
            drafts.extend(self._windows(tokens, section))

        chunks = [self._make_chunk(document, index, *draft) for index, draft in enumerate(drafts)]
        for index, chunk in enumerate(chunks):
            if index:
                chunk.previous_chunk_id = chunks[index - 1].id
            if index + 1 < len(chunks):
                chunk.next_chunk_id = chunks[index + 1].id
        return chunks

    def _windows(
        self, tokens: list[Match[str]], section: _Section
    ) -> list[tuple[int, int, int, tuple[str, ...]]]:
        step = self._settings.chunk_size_tokens - self._settings.chunk_overlap_tokens
        windows: list[tuple[int, int, int, tuple[str, ...]]] = []
        for first in range(0, len(tokens), step):
            last = min(first + self._settings.chunk_size_tokens, len(tokens))
            start = section.start + tokens[first].start()
            end = section.start + tokens[last - 1].end()
            windows.append((start, end, last - first, section.heading_path))
            if last == len(tokens):
                break
        return windows

    def _make_chunk(
        self, document: Document, index: int, start: int, end: int, token_count: int,
        heading_path: tuple[str, ...],
    ) -> Chunk:
        content = document.content[start:end]
        content_hash = sha256(content.encode("utf-8")).hexdigest()
        page_start = None
        page_end = None
        if document.metadata.page_count:
            page_start = document.content.count("\f", 0, start) + 1
            page_end = document.content.count("\f", 0, end) + 1
        source_identity = document.metadata.checksum or document.id
        identity = f"{source_identity}:{self._settings.version}:{index}:{content_hash}"
        stable_id = str(uuid5(NAMESPACE_URL, identity))
        return Chunk(
            id=stable_id,
            document_id=document.id,
            content=content,
            index=index,
            token_count=token_count,
            start_offset=start,
            end_offset=end,
            metadata=ChunkMetadata(
                page_number=page_start,
                end_page_number=page_end,
                section=" / ".join(heading_path) or None,
                heading=heading_path[-1] if heading_path else None,
                heading_path=heading_path,
                source_path=document.metadata.filename,
                mime_type=document.metadata.mime_type,
                content_hash=content_hash,
                chunker_version=self._settings.version,
            ),
        )

    @staticmethod
    def _sections(content: str, extension: str) -> list[_Section]:
        if extension.lower() not in {".md", ".markdown"}:
            return [_Section(0, len(content), ())]
        headings = list(MARKDOWN_HEADING_PATTERN.finditer(content))
        if not headings:
            return [_Section(0, len(content), ())]
        sections: list[_Section] = []
        if headings[0].start() > 0:
            sections.append(_Section(0, headings[0].start(), ()))
        path: list[str] = []
        for index, match in enumerate(headings):
            level = len(match.group(1))
            title = match.group(2).strip()
            path[level - 1 :] = [title]
            end = headings[index + 1].start() if index + 1 < len(headings) else len(content)
            sections.append(_Section(match.start(), end, tuple(path)))
        return sections
