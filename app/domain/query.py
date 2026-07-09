from dataclasses import dataclass

from app.domain.base import BaseEntity


@dataclass(slots=True)
class Query(BaseEntity):
    """Represents a user query."""

    text: str = ""