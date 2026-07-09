from typing import Any

from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health() -> dict[str, Any]:

    return {
        "status": "healthy"
    }