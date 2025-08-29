from domain.interfaces.repositories import DrawRepository
from domain.interfaces.services import DrawService
from application.dto.response import ValidationResponse


class ValidateDrawUseCase:
    """Use case for validating a draw"""

    def __init__(
            self,
            draw_repository: DrawRepository,
            draw_service: DrawService
    ):
        self.draw_repository = draw_repository
        self.draw_service = draw_service

    async def execute(self, draw_id: int) -> ValidationResponse:
        """Execute the validation use case"""

        # Get the draw from repository
        draw = await self.draw_repository.get_by_id(draw_id)
        if not draw:
            raise ValueError(f"Draw with id {draw_id} not found")

        # Validate the draw
        is_valid, errors = await self.draw_service.validate_draw(draw)

        # Calculate statistics
        statistics = {
            "total_teams": len(draw.teams),
            "total_fixtures": len(draw.fixtures),
            "fixtures_per_team": {
                team.name: len(draw.get_team_fixtures(team.id))
                for team in draw.teams
            }
        }

        return ValidationResponse(
            is_valid=is_valid,
            errors=errors,
            warnings=[],
            statistics=statistics
        )