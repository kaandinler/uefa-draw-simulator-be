from typing import List, Optional, Dict
from domain.entities import Team, Draw
from domain.value_objects import CompetitionType
from domain.interfaces.repositories import TeamRepository, DrawRepository


class InMemoryTeamRepository(TeamRepository):
    """In-memory implementation of Team repository for testing"""

    def __init__(self):
        self.teams: Dict[int, Team] = {}
        self.next_id = 1

    async def get_by_id(self, team_id: int) -> Optional[Team]:
        return self.teams.get(team_id)

    async def get_by_competition(self, competition: CompetitionType) -> List[Team]:
        # For simplicity, return all teams
        return list(self.teams.values())

    async def get_all(self) -> List[Team]:
        return list(self.teams.values())

    async def save(self, team: Team) -> Team:
        if not team.id:
            team.id = self.next_id
            self.next_id += 1
        self.teams[team.id] = team
        return team

    async def save_many(self, teams: List[Team]) -> List[Team]:
        saved_teams = []
        for team in teams:
            saved_team = await self.save(team)
            saved_teams.append(saved_team)
        return saved_teams

    async def delete(self, team_id: int) -> bool:
        if team_id in self.teams:
            del self.teams[team_id]
            return True
        return False


class InMemoryDrawRepository(DrawRepository):
    """In-memory implementation of Draw repository for testing"""

    def __init__(self):
        self.draws: Dict[int, Draw] = {}
        self.next_id = 1

    async def get_by_id(self, draw_id: int) -> Optional[Draw]:
        return self.draws.get(draw_id)

    async def get_by_competition_and_season(
            self, competition: CompetitionType, season: str
    ) -> Optional[Draw]:
        for draw in self.draws.values():
            if draw.competition == competition.value and draw.season == season:
                return draw
        return None

    async def save(self, draw: Draw) -> Draw:
        if not draw.id:
            draw.id = self.next_id
            self.next_id += 1
        self.draws[draw.id] = draw
        return draw

    async def get_latest(self, competition: CompetitionType) -> Optional[Draw]:
        competition_draws = [
            d for d in self.draws.values()
            if d.competition == competition.value
        ]
        if competition_draws:
            return max(competition_draws, key=lambda d: d.created_at or 0)
        return None