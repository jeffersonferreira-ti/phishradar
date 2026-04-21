from fastapi import FastAPI

from app.api.routes.analyze import router as analyze_router
from app.api.routes.health import router as health_router


def create_app() -> FastAPI:
    app = FastAPI(title="PhishRadar API")
    app.include_router(health_router)
    app.include_router(analyze_router)
    return app


app = create_app()
