from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from enum import Enum


class FixtureStatus(Enum):
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    POSTPONED = "postponed"


@dataclass
class Fixture:
    """Fixture entity representing a match between two teams"""
    id: Optional[int] = None
    home_team_id: int = None
    away_team_id: int = None
    matchday: Optional[int] = None
    is_home: bool = True
    scheduled_date: Optional[datetime] = None
    status: FixtureStatus = FixtureStatus.SCHEDULED
    home_score: Optional[int] = None
    away_score: Optional[int] = None

    def __post_init__(self):
        if self.home_team_id == self.away_team_id:
            raise ValueError("A team cannot play against itself")
        if self.matchday and not (1 <= self.matchday <= 8):
            raise ValueError("Matchday must be between 1 and 8")

    def involves_team(self, team_id: int) -> bool:
        """Check if a team is involved in this fixture"""
        return team_id in [self.home_team_id, self.away_team_id]

    def get_opponent_id(self, team_id: int) -> int:
        """Get the opponent team ID for a given team"""
        if team_id == self.home_team_id:
            return self.away_team_id
        elif team_id == self.away_team_id:
            return self.home_team_id
        else:
            raise ValueError(f"Team {team_id} is not in this fixture")

    def is_home_for_team(self, team_id: int) -> bool:
        """Check if a team is playing at home"""
        if team_id == self.home_team_id:
            return True
        elif team_id == self.away_team_id:
            return False
        else:
            raise ValueError(f"Team {team_id} is not in this fixture")