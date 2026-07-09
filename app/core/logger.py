import sys

from loguru import logger

from app.config.settings import get_settings

settings = get_settings()

logger.remove()

logger.add(
    sys.stdout,
    level=settings.logging.LOG_LEVEL,
    format=settings.logging.LOG_FORMAT,
)

__all__ = ["logger"]
