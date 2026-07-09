from pydantic import BaseModel


class LoggingSettings(BaseModel):
    LOG_LEVEL: str = "INFO"

    LOG_FORMAT: str = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level:<8}</level> | "
        "{name}:{function}:{line} - "
        "{message}"
    )
