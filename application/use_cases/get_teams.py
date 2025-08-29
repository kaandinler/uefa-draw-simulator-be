from typing import List
from app.domain.value_objects import CompetitionType
from app.domain.interfaces.services import TeamService
from app.application.dto.response import TeamResponse


class GetTeamsUseCase:
    """Use case for getting teams by competition"""

    def __init__(self, team_service: TeamService):
        self.team_service = team_service

    async def execute(self, competition: str) -> List[TeamResponse]:
        """Execute the get teams use case"""

        competition_type = CompetitionType(competition)
        teams = await self.team_service.get_teams_by_competition(competition_type)

        return [
            TeamResponse(
                id=team.id,
                name=team.name,
                country=team.country,
                pot=team.pot,
                coefficient=team.coefficient,
                logo_url=team.logo_url
            )
            for team in teams
        ]