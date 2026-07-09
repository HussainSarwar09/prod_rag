from dataclasses import dataclass

from app.domain.base import BaseEntity


@dataclass(slots=True)
class Answer(BaseEntity):
    """Represents an LLM response."""

    text: str = ""
