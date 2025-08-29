from dataclasses import dataclass, field
from typing import List, Dict, Set
from datetime import datetime
from .team import Team
from .fixture import Fixture


@dataclass
class Draw:
    """Draw entity representing a complete draw result"""
    id: Optional[int] = None
    competition: str = None
    season: str = None
    teams: List[Team] = field(default_factory=list)
    fixtures: List[Fixture] = field(default_factory=list)
    created_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    is_valid: bool = False
    validation_errors: List[str] = field(default_factory=list)

    def __post_init__(self):
        if self.teams and len(self.teams) != 36:
            raise ValueError("A draw must contain exactly 36 teams")

    def add_fixture(self, fixture: Fixture):
        """Add a fixture to the draw"""
        self.fixtures.append(fixture)

    def get_team_fixtures(self, team_id: int) -> List[Fixture]:
        """Get all fixtures for a specific team"""
        return [f for f in self.fixtures if f.involves_team(team_id)]

    def get_team_home_fixtures(self, team_id: int) -> List[Fixture]:
        """Get home fixtures for a team"""
        return [f for f in self.fixtures if f.home_team_id == team_id]

    def get_team_away_fixtures(self, team_id: int) -> List[Fixture]:
        """Get away fixtures for a team"""
        return [f for f in self.fixtures if f.away_team_id == team_id]

    def validate(self) -> bool:
        """Validate the draw according to UEFA rules"""
        self.validation_errors = []

        # Check if we have 36 teams
        if len(self.teams) != 36:
            self.validation_errors.append("Draw must contain exactly 36 teams")
            return False

        # Check pot distribution (9 teams per pot)
        pot_counts = {1: 0, 2: 0, 3: 0, 4: 0}
        for team in self.teams:
            pot_counts[team.pot] += 1

        for pot, count in pot_counts.items():
            if count != 9:
                self.validation_errors.append(f"Pot {pot} must contain exactly 9 teams, found {count}")

        # Check fixtures for each team
        for team in self.teams:
            team_fixtures = self.get_team_fixtures(team.id)

            # Each team must play 8 matches
            if len(team_fixtures) != 8:
                self.validation_errors.append(f"{team.name} has {len(team_fixtures)} fixtures, expected 8")

            # Each team must play 4 home and 4 away matches
            home_count = len(self.get_team_home_fixtures(team.id))
            away_count = len(self.get_team_away_fixtures(team.id))

            if home_count != 4:
                self.validation_errors.append(f"{team.name} has {home_count} home matches, expected 4")
            if away_count != 4:
                self.validation_errors.append(f"{team.name} has {away_count} away matches, expected 4")

            # Check opponent distribution by pot
            opponents_by_pot = {1: [], 2: [], 3: [], 4: []}
            for fixture in team_fixtures:
                opponent_id = fixture.get_opponent_id(team.id)
                opponent = next((t for t in self.teams if t.id == opponent_id), None)
                if opponent:
                    opponents_by_pot[opponent.pot].append(opponent)

            # Must play against 2 teams from each pot
            for pot, opponents in opponents_by_pot.items():
                if len(opponents) != 2:
                    self.validation_errors.append(
                        f"{team.name} plays against {len(opponents)} teams from pot {pot}, expected 2"
                    )

            # Check country restrictions
            country_opponents = {}
            for fixture in team_fixtures:
                opponent_id = fixture.get_opponent_id(team.id)
                opponent = next((t for t in self.teams if t.id == opponent_id), None)
                if opponent:
                    if opponent.country == team.country:
                        self.validation_errors.append(
                            f"{team.name} cannot play against {opponent.name} (same country)"
                        )
                    country_opponents.setdefault(opponent.country, []).append(opponent)

            # Maximum 2 opponents from the same country
            for country, opponents in country_opponents.items():
                if len(opponents) > 2:
                    self.validation_errors.append(
                        f"{team.name} plays against {len(opponents)} teams from {country}, maximum is 2"
                    )

        self.is_valid = len(self.validation_errors) == 0
        return self.is_valid