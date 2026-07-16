"""
Hashing utilities.
"""

from hashlib import sha256
from pathlib import Path


def sha256_file(file_path: Path) -> str:
    """Return the SHA-256 checksum of a file."""

    digest = sha256()

    with file_path.open("rb") as file:
        while chunk := file.read(8192):
            digest.update(chunk)

    return digest.hexdigest()
