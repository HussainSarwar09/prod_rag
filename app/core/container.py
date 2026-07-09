"""
Application dependency container.

This module will be responsible for creating and providing
shared services such as LLMs, embedding models, vector stores,
and rerankers.
"""

from app.config.settings import get_settings


class Container:
    """Application service container."""

    def __init__(self) -> None:
        self.settings = get_settings()


container = Container()