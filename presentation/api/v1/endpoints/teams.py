# Teams endpoints
from typing import List, Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from app.application.dto.response import TeamResponse, ErrorResponse
from app.application.use_cases import GetTeamsUseCase
from app.core.dependencies import get_teams_use_case
from app.core.exceptions import ResourceNotFoundException

router = APIRouter(prefix="/teams", tags=["teams"])

@router.get(
    "/{competition}",
    response_model=List[TeamResponse],
    summary="Get teams by competition",
    description="Retrieve all teams participating in a specific competition"
)
async def get_teams(
    competition: str,
    use_case: Annotated[GetTeamsUseCase, Depends(get_teams_use_case)]
) -> List[TeamResponse]:
    """Get teams for a specific competition"""
    try:
        teams = await use_case.execute(competition)
        return teams
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except ResourceNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message
        )