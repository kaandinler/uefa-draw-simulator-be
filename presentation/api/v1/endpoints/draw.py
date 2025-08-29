from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from application.dto.request import DrawRequest, ValidateDrawRequest
from application.dto.response import DrawResponse, ValidationResponse
from application.use_cases import PerformDrawUseCase, ValidateDrawUseCase
from core.dependencies import get_perform_draw_use_case, get_validate_draw_use_case
from core.exceptions import ValidationException, BusinessRuleException
from loguru import logger

router = APIRouter(prefix="/draw", tags=["draw"])


@router.post(
    "/",
    response_model=DrawResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Perform draw",
    description="Perform a new draw for the specified competition"
)
async def perform_draw(
        request: DrawRequest,
        background_tasks: BackgroundTasks,
        use_case: Annotated[PerformDrawUseCase, Depends(get_perform_draw_use_case)]
) -> DrawResponse:
    """Perform a new draw"""
    try:
        logger.info(f"Performing draw for {request.competition} season {request.season}")

        # Perform the draw
        result = await use_case.execute(request)

        # Add background task for additional processing if needed
        background_tasks.add_task(
            log_draw_completion,
            competition=request.competition,
            season=request.season,
            draw_id=result.id
        )

        return result

    except ValidationException as e:
        logger.error(f"Validation error: {e.message}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": e.message, "errors": e.errors}
        )
    except BusinessRuleException as e:
        logger.error(f"Business rule violation: {e.message}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.message
        )
    except Exception as e:
        logger.error(f"Unexpected error during draw: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during the draw"
        )


@router.post(
    "/validate",
    response_model=ValidationResponse,
    summary="Validate draw",
    description="Validate an existing draw against UEFA rules"
)
async def validate_draw(
        request: ValidateDrawRequest,
        use_case: Annotated[ValidateDrawUseCase, Depends(get_validate_draw_use_case)]
) -> ValidationResponse:
    """Validate an existing draw"""
    try:
        result = await use_case.execute(request.draw_id)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


async def log_draw_completion(competition: str, season: str, draw_id: int):
    """Background task to log draw completion"""
    logger.info(f"Draw completed - Competition: {competition}, Season: {season}, ID: {draw_id}")