from fastapi import APIRouter
from presentation.api.v1.endpoints import teams, draw, health

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(health.router)
api_router.include_router(teams.router)
api_router.include_router(draw.router)