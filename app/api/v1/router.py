from fastapi import APIRouter

from app.api.v1.health import router as health_router

router = APIRouter()

router.include_router(health_router)

# Future routers
# router.include_router(ingestion_router)
# router.include_router(retrieval_router)
# router.include_router(chat_router)
# router.include_router(evaluation_router)
# router.include_router(admin_router)