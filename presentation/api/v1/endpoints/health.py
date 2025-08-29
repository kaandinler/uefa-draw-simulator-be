# Health check endpoints
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from typing import Annotated
from app.core.dependencies import get_db_session

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/")
async def health_check():
    """Basic health check"""
    return {
        "status": "healthy",
        "service": "UEFA Draw API"
    }


@router.get("/ready")
async def readiness_check(
        db: Annotated[AsyncSession, Depends(get_db_session)]
):
    """Readiness check including database connectivity"""
    try:
        # Check database connectivity
        await db.execute(text("SELECT 1"))

        return {
            "status": "ready",
            "database": "connected"
        }
    except Exception as e:
        return {
            "status": "not ready",
            "database": "disconnected",
            "error": str(e)
        }
