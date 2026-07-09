from dataclasses import dataclass

from app.domain.base import BaseEntity


@dataclass(slots=True)
class Document(BaseEntity):
    """Represents a source document."""

    content: str = ""
