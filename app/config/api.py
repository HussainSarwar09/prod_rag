from pydantic import BaseModel


class APISettings(BaseModel):
    APP_NAME: str = "Production RAG"

    APP_VERSION: str = "0.1.0"

    APP_ENV: str = "development"

    DEBUG: bool = True

    API_PREFIX: str = "/api/v1"