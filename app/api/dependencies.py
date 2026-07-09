"""
Shared FastAPI dependencies.

This module contains reusable dependencies that can be injected into
API endpoints using FastAPI's dependency injection system.
"""

from typing import Annotated

from fastapi import Depends

from app.config.settings import Settings, get_settings

SettingsDependency = Annotated[
    Settings,
    Depends(get_settings),
]
