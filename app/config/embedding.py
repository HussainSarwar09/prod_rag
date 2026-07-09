from pydantic import BaseModel


class EmbeddingSettings(BaseModel):
    MODEL: str = "BAAI/bge-small-en-v1.5"

    DEVICE: str = "cpu"

    NORMALIZE: bool = True
