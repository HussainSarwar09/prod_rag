"""
Shared domain primitives.

This module contains reusable building blocks for all domain models.
"""

from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import uuid4


def generate_id() -> str:
    """Generate a unique identifier."""
    return str(uuid4())


def utc_now() -> datetime:
    """Return the current UTC timestamp."""
    return datetime.now(UTC)


@dataclass(slots=True, kw_only=True)
class BaseEntity:
    """
    Base class for all domain entities.
    """

    id: str = field(default_factory=generate_id)
    # created_at: datetime = field(default_factory=utc_now)
