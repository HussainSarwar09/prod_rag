from typing import Any

from fastapi import FastAPI

from app.api.router import router
from app.config.settings import get_settings
from app.core.lifespan import lifespan


def create_app() -> FastAPI:
    settings = get_settings()

    application = FastAPI(
        title=settings.api.APP_NAME,
        version=settings.api.APP_VERSION,
        debug=settings.api.DEBUG,
        lifespan=lifespan,
    )

    @application.get("/", tags=["Root"])
    async def root() -> dict[str, Any]:
        return {
            "application": settings.api.APP_NAME,
            "version": settings.api.APP_VERSION,
        }

    application.include_router(router)

    return application


app = create_app()