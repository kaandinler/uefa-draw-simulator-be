# Draw business logic

import random
from typing import List, Dict, Set, Tuple
from domain.entities import Team, Draw, Fixture
from domain.value_objects import CompetitionType
from domain.interfaces.services import DrawService, ValidationService
from domain.interfaces.repositories import DrawRepository, TeamRepository, FixtureRepository


class DrawServiceImpl(DrawService):
    """Implementation of draw service with UEFA rules"""

    def __init__(
            self,
            draw_repository: DrawRepository,
            team_repository: TeamRepository,
            fixture_repository: FixtureRepository,
            validation_service: ValidationService
    ):
        self.draw_repository = draw_repository
        self.team_repository = team_repository
        self.fixture_repository = fixture_repository
        self.validation_service = validation_service

    async def perform_draw(
            self, teams: List[Team], competition: CompetitionType, season: str
    ) -> Draw:
        """Perform the draw according to UEFA rules"""

        # Initialize draw
        draw = Draw(
            competition=competition.value,
            season=season,
            teams=teams,
            fixtures=[]
        )

        # Organize teams by pot
        pots = self._organize_by_pot(teams)

        # Track fixtures for each team
        team_fixtures: Dict[int, List[Fixture]] = {team.id: [] for team in teams}
        team_opponents: Dict[int, Set[int]] = {team.id: set() for team in teams}

        # Perform draw for each pot
        for pot_num in range(1, 5):
            pot_teams = pots[pot_num].copy()
            random.shuffle(pot_teams)

            for team in pot_teams:
                await self._draw_opponents_for_team(
                    team, pots, team_fixtures, team_opponents, teams
                )

        # Convert fixtures dictionary to list
        all_fixtures = []
        processed_pairs = set()

        for team_id, fixtures in team_fixtures.items():
            for fixture in fixtures:
                pair = tuple(sorted([fixture.home_team_id, fixture.away_team_id]))
                if pair not in processed_pairs:
                    all_fixtures.append(fixture)
                    processed_pairs.add(pair)

        draw.fixtures = all_fixtures

        # Validate the draw
        draw.validate()

        # Save to repository
        saved_draw = await self.draw_repository.save(draw)

        return saved_draw

    async def validate_draw(self, draw: Draw) -> Tuple[bool, List[str]]:
        """Validate a draw according to UEFA rules"""
        is_valid = draw.validate()
        return is_valid, draw.validation_errors

    def _organize_by_pot(self, teams: List[Team]) -> Dict[int, List[Team]]:
        """Organize teams by their pot number"""
        pots = {1: [], 2: [], 3: [], 4: []}
        for team in teams:
            pots[team.pot].append(team)
        return pots

    async def _draw_opponents_for_team(
            self,
            team: Team,
            pots: Dict[int, List[Team]],
            team_fixtures: Dict[int, List[Fixture]],
            team_opponents: Dict[int, Set[int]],
            all_teams: List[Team]
    ):
        """Draw opponents for a specific team"""

        # Need 2 opponents from each pot
        for pot_num in range(1, 5):
            opponents_needed = 2
            current_pot_opponents = sum(
                1 for opp_id in team_opponents[team.id]
                if any(t.id == opp_id and t.pot == pot_num for t in all_teams)
            )

            while current_pot_opponents < opponents_needed:
                # Get valid opponents from this pot
                valid_opponents = self._get_valid_opponents(
                    team, pots[pot_num], team_opponents, all_teams
                )

                if not valid_opponents:
                    raise ValueError(
                        f"Cannot find valid opponent for {team.name} from pot {pot_num}"
                    )

                # Select random opponent
                opponent = random.choice(valid_opponents)

                # Determine home/away
                is_team_home = self._determine_home_away(
                    team.id, opponent.id, team_fixtures
                )

                # Create fixtures
                if is_team_home:
                    fixture = Fixture(
                        home_team_id=team.id,
                        away_team_id=opponent.id
                    )
                else:
                    fixture = Fixture(
                        home_team_id=opponent.id,
                        away_team_id=team.id
                    )

                # Update tracking
                team_fixtures[team.id].append(fixture)
                team_fixtures[opponent.id].append(fixture)
                team_opponents[team.id].add(opponent.id)
                team_opponents[opponent.id].add(team.id)

                current_pot_opponents += 1

    def _get_valid_opponents(
            self,
            team: Team,
            pot_teams: List[Team],
            team_opponents: Dict[int, Set[int]],
            all_teams: List[Team]
    ) -> List[Team]:
        """Get list of valid opponents for a team from a specific pot"""
        valid_opponents = []

        for opponent in pot_teams:
            if opponent.id == team.id:
                continue

            if opponent.id in team_opponents[team.id]:
                continue

            # Check if opponent already has 8 matches
            if len(team_opponents[opponent.id]) >= 8:
                continue

            # Check country restrictions
            if not self._check_country_restriction(
                    team, opponent, team_opponents, all_teams
            ):
                continue

            valid_opponents.append(opponent)

        return valid_opponents

    def _check_country_restriction(
            self,
            team: Team,
            opponent: Team,
            team_opponents: Dict[int, Set[int]],
            all_teams: List[Team]
    ) -> bool:
        """Check if two teams can play against each other based on country restrictions"""

        # Same country teams cannot play
        if team.country == opponent.country:
            return False

        # Check max 2 opponents from same country for team
        team_country_opponents = sum(
            1 for opp_id in team_opponents[team.id]
            if any(t.id == opp_id and t.country == opponent.country for t in all_teams)
        )
        if team_country_opponents >= 2:
            return False

        # Check max 2 opponents from same country for opponent
        opponent_country_opponents = sum(
            1 for opp_id in team_opponents[opponent.id]
            if any(t.id == opp_id and t.country == team.country for t in all_teams)
        )
        if opponent_country_opponents >= 2:
            return False

        return True


    def _determine_home_away(
            self,
            team_id: int,
            opponent_id: int,
            team_fixtures: Dict[int, List[Fixture]]
    ) -> bool:
        """Determine if team plays at home or away"""
        team_home_count = sum(
            1 for f in team_fixtures[team_id]
            if f.home_team_id == team_id
        )
        team_away_count = len(team_fixtures[team_id]) - team_home_count

        opponent_home_count = sum(
            1 for f in team_fixtures[opponent_id]
            if f.home_team_id == opponent_id
        )
        opponent_away_count = len(team_fixtures[opponent_id]) - opponent_home_count

        # Check if team can play at home (max 4 home games)
        can_team_home = team_home_count < 4
        can_team_away = team_away_count < 4

        # Check if opponent can play away/home
        can_opponent_home = opponent_home_count < 4
        can_opponent_away = opponent_away_count < 4

        if can_team_home and can_opponent_away:
            if can_team_away and can_opponent_home:
                # Both options valid, choose randomly
                return random.choice([True, False])
            return True
        elif can_team_away and can_opponent_home:
            return False
        else:
            # Should not happen with proper validation
            return True