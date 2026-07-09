from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

from app.config.api import APISettings
from app.config.embedding import EmbeddingSettings
from app.config.llm import LLMSettings
from app.config.logging import LoggingSettings
from app.config.prompts import PromptSettings
from app.config.vectorstore import VectorStoreSettings


class Settings(BaseSettings):
    api: APISettings = APISettings()

    logging: LoggingSettings = LoggingSettings()

    llm: LLMSettings = LLMSettings()

    embeddings: EmbeddingSettings = EmbeddingSettings()

    vectorstore: VectorStoreSettings = VectorStoreSettings()

    prompts: PromptSettings = PromptSettings()

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
