from dataclasses import dataclass

from app.domain.base import BaseEntity


@dataclass(slots=True)
class Citation(BaseEntity):
    """Represents a citation."""

    source: str = ""
    page: int = 0