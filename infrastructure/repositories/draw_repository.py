from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from sqlalchemy.orm import selectinload
from app.domain.entities import Draw
from app.domain.value_objects import CompetitionType
from app.domain.interfaces.repositories import DrawRepository
from app.infrastructure.database.models import DrawModel
from app.infrastructure.repositories.mappers import DrawMapper


class DrawRepositoryImpl(DrawRepository):
    """Implementation of Draw repository using SQLAlchemy"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.mapper = DrawMapper()

    async def get_by_id(self, draw_id: int) -> Optional[Draw]:
        """Get draw by ID"""
        result = await self.session.execute(
            select(DrawModel)
            .options(selectinload(DrawModel.teams))
            .options(selectinload(DrawModel.fixtures))
            .where(DrawModel.id == draw_id)
        )
        draw_model = result.scalar_one_or_none()

        if draw_model:
            return self.mapper.to_entity(draw_model)
        return None

    async def get_by_competition_and_season(
            self, competition: CompetitionType, season: str
    ) -> Optional[Draw]:
        """Get draw by competition and season"""
        result = await self.session.execute(
            select(DrawModel)
            .options(selectinload(DrawModel.teams))
            .options(selectinload(DrawModel.fixtures))
            .where(
                DrawModel.competition == competition.value,
                DrawModel.season == season
            )
        )
        draw_model = result.scalar_one_or_none()

        if draw_model:
            return self.mapper.to_entity(draw_model)
        return None

    async def save(self, draw: Draw) -> Draw:
        """Save a draw"""
        draw_model = self.mapper.to_model(draw)

        if draw.id:
            # Update existing
            existing = await self.session.get(DrawModel, draw.id)
            if existing:
                for key, value in draw_model.__dict__.items():
                    if not key.startswith('_'):
                        setattr(existing, key, value)
                draw_model = existing
        else:
            # Create new
            self.session.add(draw_model)

        await self.session.flush()
        return self.mapper.to_entity(draw_model)

    async def get_latest(self, competition: CompetitionType) -> Optional[Draw]:
        """Get the latest draw for a competition"""
        result = await self.session.execute(
            select(DrawModel)
            .options(selectinload(DrawModel.teams))
            .options(selectinload(DrawModel.fixtures))
            .where(DrawModel.competition == competition.value)
            .order_by(desc(DrawModel.created_at))
            .limit(1)
        )
        draw_model = result.scalar_one_or_none()

        if draw_model:
            return self.mapper.to_entity(draw_model)
        return None