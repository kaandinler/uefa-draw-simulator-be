from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities import Team, Draw, Fixture
from ..value_objects import CompetitionType


class TeamRepository(ABC):
    """Repository interface for Team entity"""

    @abstractmethod
    async def get_by_id(self, team_id: int) -> Optional[Team]:
        pass

    @abstractmethod
    async def get_by_competition(self, competition: CompetitionType) -> List[Team]:
        pass

    @abstractmethod
    async def get_all(self) -> List[Team]:
        pass

    @abstractmethod
    async def save(self, team: Team) -> Team:
        pass

    @abstractmethod
    async def save_many(self, teams: List[Team]) -> List[Team]:
        pass

    @abstractmethod
    async def delete(self, team_id: int) -> bool:
        pass


class DrawRepository(ABC):
    """Repository interface for Draw entity"""

    @abstractmethod
    async def get_by_id(self, draw_id: int) -> Optional[Draw]:
        pass

    @abstractmethod
    async def get_by_competition_and_season(
            self, competition: CompetitionType, season: str
    ) -> Optional[Draw]:
        pass

    @abstractmethod
    async def save(self, draw: Draw) -> Draw:
        pass

    @abstractmethod
    async def get_latest(self, competition: CompetitionType) -> Optional[Draw]:
        pass


class FixtureRepository(ABC):
    """Repository interface for Fixture entity"""

    @abstractmethod
    async def get_by_id(self, fixture_id: int) -> Optional[Fixture]:
        pass

    @abstractmethod
    async def get_by_team(self, team_id: int) -> List[Fixture]:
        pass

    @abstractmethod
    async def save(self, fixture: Fixture) -> Fixture:
        pass

    @abstractmethod
    async def save_many(self, fixtures: List[Fixture]) -> List[Fixture]:
        pass