from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.middleware.auth import GCIPAuthMiddleware
from app.routers import food, meals, planner
from app.config import get_settings
import structlog

logger = structlog.get_logger()

def create_app() -> FastAPI:
    settings = get_settings()
    
    app = FastAPI(
        title="NutriSense AI API",
        description="Smart food intelligence API",
        version="1.0.0",
        docs_url="/docs",
        redoc_url=None,
    )

    # Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"], # In production, restrict to frontend URL
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(GCIPAuthMiddleware)

    # Routers
    app.include_router(food.router, prefix="/api/v1")
    app.include_router(meals.router, prefix="/api/v1")
    app.include_router(planner.router, prefix="/api/v1")

    @app.get("/health", tags=["Health"])
    async def health_check():
        return {"status": "ok"}
        
    @app.get("/ready", tags=["Health"])
    async def readiness_check():
        return {"status": "ready"}

    @app.on_event("startup")
    async def startup_event():
        logger.info("Application starting up")

    @app.on_event("shutdown")
    async def shutdown_event():
        logger.info("Application shutting down")
        
    return app

app = create_app()
