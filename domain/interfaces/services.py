from abc import ABC, abstractmethod
from typing import List, Dict
from ..entities import Team, Draw, Fixture
from ..value_objects import CompetitionType


class DrawService(ABC):
    """Service interface for draw operations"""

    @abstractmethod
    async def perform_draw(
            self, teams: List[Team], competition: CompetitionType, season: str
    ) -> Draw:
        pass

    @abstractmethod
    async def validate_draw(self, draw: Draw) -> tuple[bool, List[str]]:
        pass


class TeamService(ABC):
    """Service interface for team operations"""

    @abstractmethod
    async def get_teams_by_competition(self, competition: CompetitionType) -> List[Team]:
        pass

    @abstractmethod
    async def organize_teams_by_pot(self, teams: List[Team]) -> Dict[int, List[Team]]:
        pass


class ValidationService(ABC):
    """Service interface for validation operations"""

    @abstractmethod
    def validate_team_compatibility(self, team1: Team, team2: Team) -> bool:
        pass

    @abstractmethod
    def validate_fixture_constraints(
            self, team: Team, fixtures: List[Fixture], teams: List[Team]
    ) -> tuple[bool, List[str]]:
        pass