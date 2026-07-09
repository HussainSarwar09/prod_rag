from pydantic import BaseModel


class PromptSettings(BaseModel):
    SYSTEM_PROMPT_VERSION: str = "v1"
