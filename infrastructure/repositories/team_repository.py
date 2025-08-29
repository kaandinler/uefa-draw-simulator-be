from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from domain.entities import Team
from domain.value_objects import CompetitionType
from domain.interfaces.repositories import TeamRepository
from infrastructure.database.models import TeamModel
from infrastructure.repositories.mappers import TeamMapper


class TeamRepositoryImpl(TeamRepository):
    """Implementation of Team repository using SQLAlchemy"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.mapper = TeamMapper()

    async def get_by_id(self, team_id: int) -> Optional[Team]:
        """Get team by ID"""
        result = await self.session.execute(
            select(TeamModel).where(TeamModel.id == team_id)
        )
        team_model = result.scalar_one_or_none()

        if team_model:
            return self.mapper.to_entity(team_model)
        return None

    async def get_by_competition(self, competition: CompetitionType) -> List[Team]:
        """Get teams by competition"""
        # In a real implementation, you would filter by competition
        # For now, return all teams
        result = await self.session.execute(select(TeamModel))
        team_models = result.scalars().all()

        return [self.mapper.to_entity(model) for model in team_models]

    async def get_all(self) -> List[Team]:
        """Get all teams"""
        result = await self.session.execute(select(TeamModel))
        team_models = result.scalars().all()

        return [self.mapper.to_entity(model) for model in team_models]

    async def save(self, team: Team) -> Team:
        """Save a team"""
        team_model = self.mapper.to_model(team)

        if team.id:
            # Update existing
            existing = await self.session.get(TeamModel, team.id)
            if existing:
                for key, value in team_model.__dict__.items():
                    if not key.startswith('_'):
                        setattr(existing, key, value)
                team_model = existing
        else:
            # Create new
            self.session.add(team_model)

        await self.session.flush()
        return self.mapper.to_entity(team_model)

    async def save_many(self, teams: List[Team]) -> List[Team]:
        """Save multiple teams"""
        saved_teams = []
        for team in teams:
            saved_team = await self.save(team)
            saved_teams.append(saved_team)
        return saved_teams

    async def delete(self, team_id: int) -> bool:
        """Delete a team"""
        result = await self.session.execute(
            delete(TeamModel).where(TeamModel.id == team_id)
        )
        return result.rowcount > 0