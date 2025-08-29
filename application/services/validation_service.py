from typing import List, Tuple
from app.domain.entities import Team, Fixture
from app.domain.interfaces.services import ValidationService


class ValidationServiceImpl(ValidationService):
    """Implementation of validation service"""

    def validate_team_compatibility(self, team1: Team, team2: Team) -> bool:
        """Check if two teams can play against each other"""
        # Teams from same country cannot play each other
        if team1.country == team2.country:
            return False
        return True

    def validate_fixture_constraints(
            self, team: Team, fixtures: List[Fixture], teams: List[Team]
    ) -> Tuple[bool, List[str]]:
        """Validate fixture constraints for a team"""
        errors = []

        # Check total number of fixtures
        if len(fixtures) != 8:
            errors.append(f"Team must have exactly 8 fixtures, found {len(fixtures)}")

        # Check home/away balance
        home_count = sum(1 for f in fixtures if f.home_team_id == team.id)
        away_count = sum(1 for f in fixtures if f.away_team_id == team.id)

        if home_count != 4:
            errors.append(f"Team must have 4 home games, found {home_count}")
        if away_count != 4:
            errors.append(f"Team must have 4 away games, found {away_count}")

        # Check opponents by pot
        opponents_by_pot = {1: 0, 2: 0, 3: 0, 4: 0}
        country_opponents = {}

        for fixture in fixtures:
            opponent_id = fixture.get_opponent_id(team.id)
            opponent = next((t for t in teams if t.id == opponent_id), None)

            if opponent:
                # Count by pot
                opponents_by_pot[opponent.pot] += 1

                # Count by country
                if opponent.country not in country_opponents:
                    country_opponents[opponent.country] = 0
                country_opponents[opponent.country] += 1

        # Check pot distribution (2 from each pot)
        for pot, count in opponents_by_pot.items():
            if count != 2:
                errors.append(f"Team must play 2 teams from pot {pot}, found {count}")

        # Check country restrictions (max 2 from same country)
        for country, count in country_opponents.items():
            if count > 2:
                errors.append(f"Team can play max 2 teams from {country}, found {count}")

        return len(errors) == 0, errors