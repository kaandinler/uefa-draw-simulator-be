from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.config import settings
from app.core.dependencies import db_connection
from app.core.logging import setup_logging
from app.presentation.api.v1.router import api_router
from app.presentation.middleware.cors import setup_cors
from app.presentation.middleware.error_handler import setup_exception_handlers
from app.presentation.middleware.logging import setup_logging_middleware
from app.infrastructure.repositories.in_memory_repository import (
    InMemoryTeamRepository
)
from app.domain.entities import Team
from loguru import logger

# Sample teams data
SAMPLE_TEAMS = [
    # Pot 1
    {"id": 1, "name": "Paris Saint-Germain", "country": "FRA", "pot": 1, "coefficient": 150.0},
    {"id": 2, "name": "Real Madrid", "country": "ESP", "pot": 1, "coefficient": 148.0},
    {"id": 3, "name": "Manchester City", "country": "ENG", "pot": 1, "coefficient": 145.0},
    {"id": 4, "name": "Bayern München", "country": "GER", "pot": 1, "coefficient": 143.0},
    {"id": 5, "name": "Liverpool", "country": "ENG", "pot": 1, "coefficient": 141.0},
    {"id": 6, "name": "Inter Milano", "country": "ITA", "pot": 1, "coefficient": 139.0},
    {"id": 7, "name": "Chelsea", "country": "ENG", "pot": 1, "coefficient": 137.0},
    {"id": 8, "name": "Borussia Dortmund", "country": "GER", "pot": 1, "coefficient": 135.0},
    {"id": 9, "name": "Barcelona", "country": "ESP", "pot": 1, "coefficient": 133.0},
    # Add remaining teams (Pots 2-4) here...
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logger.info("Starting UEFA Draw API...")

    # Setup logging
    setup_logging()

    # Initialize database
    try:
        await db_connection.create_tables()
        logger.info("Database tables created successfully")

        # Load sample data if in development mode
        if settings.DEBUG:
            repo = InMemoryTeamRepository()
            for team_data in SAMPLE_TEAMS:
                team = Team(**team_data)
                await repo.save(team)
            logger.info("Sample data loaded")

    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")

    yield

    # Shutdown
    logger.info("Shutting down UEFA Draw API...")
    await db_connection.close()


# Create FastAPI application
def create_app() -> FastAPI:
    """Create and configure FastAPI application"""

    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.APP_VERSION,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan
    )

    # Setup middleware
    setup_cors(app)
    setup_exception_handlers(app)
    setup_logging_middleware(app)

    # Include API router
    app.include_router(api_router, prefix=settings.API_V1_STR)

    # Root endpoint
    @app.get("/")
    async def root():
        return {
            "name": settings.PROJECT_NAME,
            "version": settings.APP_VERSION,
            "docs": "/docs",
            "health": f"{settings.API_V1_STR}/health"
        }

    return app


# Create application instance
app = create_app()

# For running with uvicorn
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )