from domain.entities import Team, Draw, Fixture
from infrastructure.database.models import TeamModel, DrawModel, FixtureModel


class TeamMapper:
    """Mapper for Team entity and model"""

    def to_entity(self, model: TeamModel) -> Team:
        """Convert model to entity"""
        return Team(
            id=model.id,
            name=model.name,
            country=model.country,
            pot=model.pot,
            coefficient=model.coefficient,
            logo_url=model.logo_url,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    def to_model(self, entity: Team) -> TeamModel:
        """Convert entity to model"""
        return TeamModel(
            id=entity.id,
            name=entity.name,
            country=entity.country,
            pot=entity.pot,
            coefficient=entity.coefficient,
            logo_url=entity.logo_url
        )


class FixtureMapper:
    """Mapper for Fixture entity and model"""

    def to_entity(self, model: FixtureModel) -> Fixture:
        """Convert model to entity"""
        return Fixture(
            id=model.id,
            home_team_id=model.home_team_id,
            away_team_id=model.away_team_id,
            matchday=model.matchday,
            scheduled_date=model.scheduled_date,
            status=model.status,
            home_score=model.home_score,
            away_score=model.away_score
        )

    def to_model(self, entity: Fixture) -> FixtureModel:
        """Convert entity to model"""
        return FixtureModel(
            id=entity.id,
            home_team_id=entity.home_team_id,
            away_team_id=entity.away_team_id,
            matchday=entity.matchday,
            scheduled_date=entity.scheduled_date,
            status=entity.status.value if hasattr(entity.status, 'value') else entity.status,
            home_score=entity.home_score,
            away_score=entity.away_score
        )


class DrawMapper:
    """Mapper for Draw entity and model"""

    def __init__(self):
        self.team_mapper = TeamMapper()
        self.fixture_mapper = FixtureMapper()

    def to_entity(self, model: DrawModel) -> Draw:
        """Convert model to entity"""
        teams = [self.team_mapper.to_entity(t) for t in model.teams]
        fixtures = [self.fixture_mapper.to_entity(f) for f in model.fixtures]

        return Draw(
            id=model.id,
            competition=model.competition,
            season=model.season,
            teams=teams,
            fixtures=fixtures,
            created_at=model.created_at,
            completed_at=model.completed_at,
            is_valid=model.is_valid
        )

    def to_model(self, entity: Draw) -> DrawModel:
        """Convert entity to model"""
        return DrawModel(
            id=entity.id,
            competition=entity.competition,
            season=entity.season,
            is_valid=entity.is_valid,
            completed_at=entity.completed_at
        )