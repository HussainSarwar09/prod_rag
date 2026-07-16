from enum import StrEnum


class DocumentStatus(StrEnum):
    """Represents the lifecycle state of a document."""

    RECEIVED = "received"
    LOADING = "loading"
    LOADED = "loaded"
    FAILED = "failed"
