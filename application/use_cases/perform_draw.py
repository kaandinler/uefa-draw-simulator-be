from datetime import datetime
from domain.entities import Team
from domain.value_objects import CompetitionType
from domain.interfaces.services import DrawService
from application.dto.request import DrawRequest
from application.dto.response import DrawResponse, TeamDrawResult, TeamResponse, FixtureResponse


class PerformDrawUseCase:
    """Use case for performing a draw"""

    def __init__(self, draw_service: DrawService):
        self.draw_service = draw_service

    async def execute(self, request: DrawRequest) -> DrawResponse:
        """Execute the draw use case"""

        # Convert request DTOs to domain entities
        teams = [
            Team(
                id=team_req.id,
                name=team_req.name,
                country=team_req.country,
                pot=team_req.pot,
                coefficient=team_req.coefficient,
                logo_url=team_req.logo_url
            )
            for team_req in request.teams
        ]

        # Perform the draw
        competition_type = CompetitionType(request.competition)
        draw = await self.draw_service.perform_draw(
            teams, competition_type, request.season
        )

        # Convert to response DTO
        results = []
        for team in draw.teams:
            team_fixtures = draw.get_team_fixtures(team.id)

            fixture_responses = []
            for fixture in team_fixtures:
                opponent_id = fixture.get_opponent_id(team.id)
                opponent = next(t for t in draw.teams if t.id == opponent_id)

                fixture_responses.append(FixtureResponse(
                    opponent_id=opponent.id,
                    opponent_name=opponent.name,
                    opponent_country=opponent.country,
                    is_home=fixture.home_team_id == team.id,
                    matchday=fixture.matchday,
                    scheduled_date=fixture.scheduled_date
                ))

            results.append(TeamDrawResult(
                team=TeamResponse(
                    id=team.id,
                    name=team.name,
                    country=team.country,
                    pot=team.pot,
                    coefficient=team.coefficient,
                    logo_url=team.logo_url
                ),
                fixtures=fixture_responses,
                home_games_count=len(draw.get_team_home_fixtures(team.id)),
                away_games_count=len(draw.get_team_away_fixtures(team.id))
            ))

        return DrawResponse(
            id=draw.id,
            competition=draw.competition,
            season=draw.season,
            results=results,
            total_fixtures=len(draw.fixtures),
            created_at=draw.created_at or datetime.utcnow(),
            is_valid=draw.is_valid,
            validation_errors=draw.validation_errors
        )