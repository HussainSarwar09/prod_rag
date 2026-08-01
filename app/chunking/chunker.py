"""Production-style document chunking strategies and selector."""

from __future__ import annotations

import json
from dataclasses import dataclass
from hashlib import sha256
from re import DOTALL, MULTILINE, compile, finditer
from typing import Literal, cast
from uuid import NAMESPACE_URL, uuid5

from app.config.chunking import (
    ChunkingSettings,
    ChunkingStrategySettings,
    CodeChunkingStrategySettings,
    FileTypeChunkingPolicy,
    JsonChunkingStrategySettings,
    MarkdownChunkingStrategySettings,
    ParagraphChunkingStrategySettings,
    SentenceChunkingStrategySettings,
    StrategyType,
    TokenWindowChunkingStrategySettings,
)
from app.domain.chunk import Chunk
from app.domain.chunk_metadata import ChunkMetadata
from app.domain.document import Document

TOKEN_PATTERN = compile(r"\S+")
MARKDOWN_HEADING_PATTERN = compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$", MULTILINE)
SENTENCE_PATTERN = compile(r".+?(?:[.!?](?=\s|$)|\n{2,}|$)", DOTALL)
PARAGRAPH_PATTERN = compile(r"\S.*?(?:\n\s*\n|$)", DOTALL)
JSON_PROPERTY_PATTERN = compile(r'^\s*"([^"]+)"\s*:', MULTILINE)
CODE_BLOCK_PATTERN = compile(
    r"^(?:class\s+\w+|def\s+\w+|async\s+def\s+\w+|function\s+\w+|"
    r"(?:public|private|protected)\s+\w[\w<>\[\]]*\s+\w+\s*\(|"
    r"func\s+\w+)",
    MULTILINE,
)

CODE_EXTENSIONS = {
    ".py",
    ".js",
    ".ts",
    ".tsx",
    ".jsx",
    ".java",
    ".kt",
    ".go",
    ".rb",
    ".php",
    ".cs",
    ".cpp",
    ".c",
    ".h",
    ".hpp",
    ".rs",
    ".swift",
    ".scala",
}


@dataclass(frozen=True, slots=True)
class _Section:
    start: int
    end: int
    heading_path: tuple[str, ...] = ()
    label: str | None = None


@dataclass(frozen=True, slots=True)
class _Boundary:
    start: int
    end: int
    token_count: int
    heading_path: tuple[str, ...] = ()
    label: str | None = None


class _BaseChunkingStrategy:
    strategy_name: StrategyType

    def __init__(self, settings: ChunkingStrategySettings, global_version: str) -> None:
        self._settings = settings
        self._global_version = global_version
        chunk_size = settings.chunk_size_tokens
        chunk_overlap = settings.chunk_overlap_tokens
        if chunk_overlap >= chunk_size:
            raise ValueError("chunk_overlap_tokens must be smaller than chunk_size_tokens.")

    def chunk(self, document: Document) -> list[Chunk]:
        drafts = self._draft_chunks(document)
        chunks = [self._make_chunk(document, index, draft) for index, draft in enumerate(drafts)]
        for index, chunk in enumerate(chunks):
            if index:
                chunk.previous_chunk_id = chunks[index - 1].id
            if index + 1 < len(chunks):
                chunk.next_chunk_id = chunks[index + 1].id
        return chunks

    def _draft_chunks(self, document: Document) -> list[_Boundary]:
        raise NotImplementedError

    def _version(self) -> str:
        return f"{self._global_version}:{self.strategy_name}:{self._settings.version_suffix}"

    def _split_token_windows(self, content: str, sections: list[_Section]) -> list[_Boundary]:
        step = self._settings.chunk_size_tokens - self._settings.chunk_overlap_tokens
        windows: list[_Boundary] = []
        for section in sections:
            tokens = list(finditer(TOKEN_PATTERN, content[section.start : section.end]))
            if not tokens:
                continue
            for first in range(0, len(tokens), step):
                last = min(first + self._settings.chunk_size_tokens, len(tokens))
                windows.append(
                    _Boundary(
                        start=section.start + tokens[first].start(),
                        end=section.start + tokens[last - 1].end(),
                        token_count=last - first,
                        heading_path=section.heading_path,
                        label=section.label,
                    )
                )
                if last == len(tokens):
                    break
        return windows

    def _windows_from_units(
        self,
        content: str,
        units: list[_Boundary],
        *,
        max_units_per_chunk: int | None = None,
    ) -> list[_Boundary]:
        if not units:
            return []
        max_units = max_units_per_chunk or len(units)
        chunks: list[_Boundary] = []
        index = 0
        carry_overlap_start = 0
        while index < len(units):
            start_index = carry_overlap_start if chunks else index
            token_total = 0
            end_index = start_index
            while end_index < len(units):
                next_total = token_total + units[end_index].token_count
                too_many_units = end_index - start_index + 1 > max_units
                if next_total > self._settings.chunk_size_tokens and end_index > start_index:
                    break
                if too_many_units and end_index > start_index:
                    break
                token_total = next_total
                end_index += 1
                if token_total >= self._settings.chunk_size_tokens:
                    break

            selected = units[start_index:end_index]
            chunks.append(
                _Boundary(
                    start=selected[0].start,
                    end=selected[-1].end,
                    token_count=token_total,
                    heading_path=selected[-1].heading_path,
                    label=selected[-1].label,
                )
            )
            if end_index >= len(units):
                break

            overlap_tokens = 0
            overlap_start = end_index
            while (
                overlap_start > start_index and overlap_tokens < self._settings.chunk_overlap_tokens
            ):
                overlap_start -= 1
                overlap_tokens += units[overlap_start].token_count
            carry_overlap_start = overlap_start
            index = end_index
        return chunks

    def _make_chunk(self, document: Document, index: int, boundary: _Boundary) -> Chunk:
        content = document.content[boundary.start : boundary.end]
        content_hash = sha256(content.encode("utf-8")).hexdigest()
        page_start = None
        page_end = None
        if document.metadata.page_count:
            page_start = document.content.count("\f", 0, boundary.start) + 1
            page_end = document.content.count("\f", 0, boundary.end) + 1
        source_identity = document.metadata.checksum or document.id
        identity = f"{source_identity}:{self._version()}:{index}:{content_hash}"
        stable_id = str(uuid5(NAMESPACE_URL, identity))
        return Chunk(
            id=stable_id,
            document_id=document.id,
            content=content,
            index=index,
            token_count=boundary.token_count,
            start_offset=boundary.start,
            end_offset=boundary.end,
            metadata=ChunkMetadata(
                page_number=page_start,
                end_page_number=page_end,
                section=" / ".join(boundary.heading_path) or boundary.label,
                heading=boundary.heading_path[-1] if boundary.heading_path else None,
                heading_path=boundary.heading_path,
                source_path=document.metadata.filename,
                mime_type=document.metadata.mime_type,
                content_hash=content_hash,
                chunker_version=self._version(),
                chunking_strategy=self.strategy_name,
            ),
        )


class TokenWindowChunkingStrategy(_BaseChunkingStrategy):
    strategy_name: Literal["token_window"] = "token_window"

    def __init__(self, settings: TokenWindowChunkingStrategySettings, global_version: str) -> None:
        super().__init__(settings, global_version)

    def _draft_chunks(self, document: Document) -> list[_Boundary]:
        return self._split_token_windows(document.content, [_Section(0, len(document.content))])


class MarkdownChunkingStrategy(_BaseChunkingStrategy):
    strategy_name: Literal["markdown"] = "markdown"

    def __init__(self, settings: MarkdownChunkingStrategySettings, global_version: str) -> None:
        super().__init__(settings, global_version)

    def _draft_chunks(self, document: Document) -> list[_Boundary]:
        sections = self._markdown_sections(document.content, document.metadata.extension)
        return self._split_token_windows(document.content, sections)

    @staticmethod
    def _markdown_sections(content: str, extension: str) -> list[_Section]:
        if extension.lower() not in {".md", ".markdown"}:
            return [_Section(0, len(content))]
        headings = list(MARKDOWN_HEADING_PATTERN.finditer(content))
        if not headings:
            return [_Section(0, len(content))]
        sections: list[_Section] = []
        if headings[0].start() > 0:
            sections.append(_Section(0, headings[0].start()))
        path: list[str] = []
        for index, match in enumerate(headings):
            level = len(match.group(1))
            title = match.group(2).strip()
            path[level - 1 :] = [title]
            end = headings[index + 1].start() if index + 1 < len(headings) else len(content)
            sections.append(_Section(match.start(), end, tuple(path), title))
        return sections


class SentenceChunkingStrategy(_BaseChunkingStrategy):
    strategy_name: Literal["sentence"] = "sentence"

    def __init__(self, settings: SentenceChunkingStrategySettings, global_version: str) -> None:
        super().__init__(settings, global_version)

    def _draft_chunks(self, document: Document) -> list[_Boundary]:
        settings = cast(SentenceChunkingStrategySettings, self._settings)
        units = [
            _Boundary(
                start=match.start(), end=match.end(), token_count=self._token_count(match.group())
            )
            for match in SENTENCE_PATTERN.finditer(document.content)
            if match.group().strip()
        ]
        return self._windows_from_units(
            document.content,
            units,
            max_units_per_chunk=settings.max_sentences_per_chunk,
        )

    @staticmethod
    def _token_count(text: str) -> int:
        return len(list(finditer(TOKEN_PATTERN, text)))


class ParagraphChunkingStrategy(_BaseChunkingStrategy):
    strategy_name: Literal["paragraph"] = "paragraph"

    def __init__(self, settings: ParagraphChunkingStrategySettings, global_version: str) -> None:
        super().__init__(settings, global_version)

    def _draft_chunks(self, document: Document) -> list[_Boundary]:
        settings = cast(ParagraphChunkingStrategySettings, self._settings)
        units = [
            _Boundary(
                start=match.start(), end=match.end(), token_count=self._token_count(match.group())
            )
            for match in PARAGRAPH_PATTERN.finditer(document.content)
            if match.group().strip()
        ]
        return self._windows_from_units(
            document.content,
            units,
            max_units_per_chunk=settings.max_paragraphs_per_chunk,
        )

    @staticmethod
    def _token_count(text: str) -> int:
        return len(list(finditer(TOKEN_PATTERN, text)))


class JsonChunkingStrategy(_BaseChunkingStrategy):
    strategy_name: Literal["json"] = "json"

    def __init__(self, settings: JsonChunkingStrategySettings, global_version: str) -> None:
        super().__init__(settings, global_version)

    def _draft_chunks(self, document: Document) -> list[_Boundary]:
        sections = self._json_sections(document.content)
        return self._split_token_windows(document.content, sections)

    def _json_sections(self, content: str) -> list[_Section]:
        try:
            parsed = json.loads(content)
        except json.JSONDecodeError:
            return [_Section(0, len(content), label="json-fallback")]

        if isinstance(parsed, dict):
            matches = list(JSON_PROPERTY_PATTERN.finditer(content))
            if not matches:
                return [_Section(0, len(content), label="json-object")]
            sections: list[_Section] = []
            for index, match in enumerate(matches):
                end = matches[index + 1].start() if index + 1 < len(matches) else len(content)
                sections.append(_Section(match.start(), end, label=f"json:{match.group(1)}"))
            return sections
        if isinstance(parsed, list):
            return self._json_array_sections(content)
        return [_Section(0, len(content), label="json-scalar")]

    def _json_array_sections(self, content: str) -> list[_Section]:
        lines = content.splitlines(keepends=True)
        sections: list[_Section] = []
        start = 0
        offset = 0
        item_start = None
        depth = 0
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("[") and item_start is None:
                item_start = offset
            depth += line.count("{") + line.count("[")
            depth -= line.count("}") + line.count("]")
            if stripped.endswith(",") or stripped.endswith("]") or depth == 1:
                if item_start is None:
                    item_start = start
                if offset + len(line) > item_start:
                    sections.append(_Section(item_start, offset + len(line), label="json:item"))
                item_start = offset + len(line)
            offset += len(line)
        return sections or [_Section(0, len(content), label="json-array")]


class CodeChunkingStrategy(_BaseChunkingStrategy):
    strategy_name: Literal["code"] = "code"

    def __init__(self, settings: CodeChunkingStrategySettings, global_version: str) -> None:
        super().__init__(settings, global_version)

    def _draft_chunks(self, document: Document) -> list[_Boundary]:
        sections = self._code_sections(document.content, document.metadata.extension)
        return self._split_token_windows(document.content, sections)

    def _code_sections(self, content: str, extension: str) -> list[_Section]:
        if extension.lower() not in CODE_EXTENSIONS:
            return [_Section(0, len(content), label="code-fallback")]
        matches = list(CODE_BLOCK_PATTERN.finditer(content))
        if not matches:
            return [_Section(0, len(content), label="code-module")]
        sections: list[_Section] = []
        if matches[0].start() > 0:
            sections.append(_Section(0, matches[0].start(), label="code-preamble"))
        for index, match in enumerate(matches):
            end = matches[index + 1].start() if index + 1 < len(matches) else len(content)
            label = match.group().splitlines()[0].strip()
            sections.append(_Section(match.start(), end, label=label))
        return sections


class DocumentChunker:
    """Select a chunking strategy per document using enterprise-style policies."""

    def __init__(self, settings: ChunkingSettings | None = None) -> None:
        self._settings = settings or ChunkingSettings()
        self._strategies: dict[StrategyType, _BaseChunkingStrategy] = {
            "token_window": TokenWindowChunkingStrategy(
                self._settings.token_window, self._settings.version
            ),
            "sentence": SentenceChunkingStrategy(self._settings.sentence, self._settings.version),
            "paragraph": ParagraphChunkingStrategy(
                self._settings.paragraph, self._settings.version
            ),
            "markdown": MarkdownChunkingStrategy(self._settings.markdown, self._settings.version),
            "json": JsonChunkingStrategy(self._settings.json_strategy, self._settings.version),
            "code": CodeChunkingStrategy(self._settings.code, self._settings.version),
        }

    def chunk(self, document: Document) -> list[Chunk]:
        strategy_name = self.resolve_strategy(document)
        return self._strategies[strategy_name].chunk(document)

    def resolve_strategy(self, document: Document) -> StrategyType:
        policy = self._policy_for(document)
        strategy = policy.strategy if policy else self._settings.default_strategy
        if strategy != "auto":
            return strategy
        return self._auto_strategy(document)

    def _policy_for(self, document: Document) -> FileTypeChunkingPolicy | None:
        candidates = [
            document.metadata.extension.lower(),
            document.metadata.mime_type.lower(),
        ]
        for candidate in candidates:
            if candidate in self._settings.file_type_policies:
                return self._settings.file_type_policies[candidate]
        return None

    def _auto_strategy(self, document: Document) -> StrategyType:
        extension = document.metadata.extension.lower()
        mime_type = document.metadata.mime_type.lower()
        if extension in {".md", ".markdown"}:
            return "markdown"
        if extension in {".json", ".jsonl"} or "json" in mime_type:
            return "json"
        if extension in CODE_EXTENSIONS or "python" in mime_type or "javascript" in mime_type:
            return "code"
        if extension == ".pdf" or mime_type == "application/pdf":
            return "sentence"
        if extension in {".txt", ".rst"} or mime_type.startswith("text/"):
            return "paragraph"
        return "token_window"
