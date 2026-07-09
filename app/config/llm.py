from pydantic import BaseModel


class LLMSettings(BaseModel):
    PROVIDER: str = "ollama"

    MODEL: str = "qwen3"

    TEMPERATURE: float = 0.0

    MAX_TOKENS: int = 2048
