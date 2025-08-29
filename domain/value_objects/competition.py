from enum import Enum
from dataclasses import dataclass


class CompetitionType(Enum):
    CHAMPIONS_LEAGUE = "champions_league"
    EUROPA_LEAGUE = "europa_league"
    CONFERENCE_LEAGUE = "conference_league"


@dataclass(frozen=True)
class Competition:
    """Value object representing a competition"""
    type: CompetitionType
    season: str
    name: str

    @property
    def full_name(self) -> str:
        names = {
            CompetitionType.CHAMPIONS_LEAGUE: "UEFA Champions League",
            CompetitionType.EUROPA_LEAGUE: "UEFA Europa League",
            CompetitionType.CONFERENCE_LEAGUE: "UEFA Conference League"
        }
        return f"{names.get(self.type, 'Unknown')} {self.season}"

    def __str__(self):
        return self.full_name