# Team business logic

from typing import List, Dict
from app.domain.entities import Team
from app.domain.value_objects import CompetitionType
from app.domain.interfaces.services import TeamService
from app.domain.interfaces.repositories import TeamRepository


class TeamServiceImpl(TeamService):
    """Implementation of team service"""

    def __init__(self, team_repository: TeamRepository):
        self.team_repository = team_repository

    async def get_teams_by_competition(
            self, competition: CompetitionType
    ) -> List[Team]:
        """Get all teams for a specific competition"""
        return await self.team_repository.get_by_competition(competition)

    async def organize_teams_by_pot(
            self, teams: List[Team]
    ) -> Dict[int, List[Team]]:
        """Organize teams by their pot number"""
        pots = {1: [], 2: [], 3: [], 4: []}

        # Sort teams by coefficient within each pot
        for team in sorted(teams, key=lambda t: t.coefficient, reverse=True):
            pots[team.pot].append(team)

        return pots
