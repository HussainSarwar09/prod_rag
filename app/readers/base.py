"""
Base reader abstraction.
"""

from abc import ABC, abstractmethod
from pathlib import Path


class BaseReader(ABC):
    """
    Reads a document and returns normalized text.
    """

    @abstractmethod
    def read(self, file_path: Path) -> str:
        """
        Read a file.
        """
