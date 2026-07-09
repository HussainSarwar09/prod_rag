from pydantic import BaseModel


class VectorStoreSettings(BaseModel):
    PROVIDER: str = "chroma"

    PERSIST_DIRECTORY: str = "./chroma"

    COLLECTION_NAME: str = "documents"
