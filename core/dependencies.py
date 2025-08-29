# Dependency injection container

from typing import AsyncGenerator, Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database.connection import DatabaseConnection
from app.infrastructure.repositories.team_repository import TeamRepositoryImpl
from app.infrastructure.repositories.draw_repository import DrawRepositoryImpl
from app.infrastructure.repositories.in_memory_repository import (
    InMemoryTeamRepository, InMemoryDrawRepository
)
from app.application.services import (
    DrawServiceImpl, TeamServiceImpl, ValidationServiceImpl
)
from app.application.use_cases import (
    PerformDrawUseCase, ValidateDrawUseCase, GetTeamsUseCase
)
from app.core.config import settings

# Database connection instance
db_connection = DatabaseConnection(settings.DATABASE_URL)

# Dependency for database session
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Get database session"""
    async for session in db_connection.get_session():
        yield session

# Repository dependencies
async def get_team_repository(
    session: Annotated[AsyncSession, Depends(get_db_session)]
) -> TeamRepositoryImpl:
    """Get team repository instance"""
    return TeamRepositoryImpl(session)

async def get_draw_repository(
    session: Annotated[AsyncSession, Depends(get_db_session)]
) -> DrawRepositoryImpl:
    """Get draw repository instance"""
    return DrawRepositoryImpl(session)

# For testing/development with in-memory repositories
def get_in_memory_team_repository() -> InMemoryTeamRepository:
    """Get in-memory team repository"""
    return InMemoryTeamRepository()

def get_in_memory_draw_repository() -> InMemoryDrawRepository:
    """Get in-memory draw repository"""
    return InMemoryDrawRepository()

# Service dependencies
async def get_validation_service() -> ValidationServiceImpl:
    """Get validation service instance"""
    return ValidationServiceImpl()

async def get_team_service(
    team_repository: Annotated[TeamRepositoryImpl, Depends(get_team_repository)]
) -> TeamServiceImpl:
    """Get team service instance"""
    return TeamServiceImpl(team_repository)

async def get_draw_service(
    draw_repository: Annotated[DrawRepositoryImpl, Depends(get_draw_repository)],
    team_repository: Annotated[TeamRepositoryImpl, Depends(get_team_repository)],
    validation_service: Annotated[ValidationServiceImpl, Depends(get_validation_service)]
) -> DrawServiceImpl:
    """Get draw service instance"""
    # Note: fixture_repository would be injected here too in full implementation
    return DrawServiceImpl(
        draw_repository=draw_repository,
        team_repository=team_repository,
        fixture_repository=None,  # Simplified for this example
        validation_service=validation_service
    )

# Use case dependencies
async def get_perform_draw_use_case(
    draw_service: Annotated[DrawServiceImpl, Depends(get_draw_service)]
) -> PerformDrawUseCase:
    """Get perform draw use case"""
    return PerformDrawUseCase(draw_service)

async def get_validate_draw_use_case(
    draw_repository: Annotated[DrawRepositoryImpl, Depends(get_draw_repository)],
    draw_service: Annotated[DrawServiceImpl, Depends(get_draw_service)]
) -> ValidateDrawUseCase:
    """Get validate draw use case"""
    return ValidateDrawUseCase(draw_repository, draw_service)

async def get_teams_use_case(
    team_service: Annotated[TeamServiceImpl, Depends(get_team_service)]
) -> GetTeamsUseCase:
    """Get teams use case"""
    return GetTeamsUseCase(team_service)
