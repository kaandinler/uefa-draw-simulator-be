# Error handling middleware
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from app.core.exceptions import (
    DomainException,
    ResourceNotFoundException,
    ValidationException,
    BusinessRuleException,
    ConflictException
)
from loguru import logger


def setup_exception_handlers(app: FastAPI) -> None:
    """Configure exception handlers"""

    @app.exception_handler(ResourceNotFoundException)
    async def resource_not_found_handler(request: Request, exc: ResourceNotFoundException):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "error": exc.code,
                "message": exc.message,
                "resource": exc.resource,
                "identifier": str(exc.identifier)
            }
        )

    @app.exception_handler(ValidationException)
    async def validation_exception_handler(request: Request, exc: ValidationException):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "error": exc.code,
                "message": exc.message,
                "errors": exc.errors
            }
        )

    @app.exception_handler(BusinessRuleException)
    async def business_rule_handler(request: Request, exc: BusinessRuleException):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": exc.code,
                "message": exc.message
            }
        )

    @app.exception_handler(ConflictException)
    async def conflict_handler(request: Request, exc: ConflictException):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "error": exc.code,
                "message": exc.message
            }
        )

    @app.exception_handler(DomainException)
    async def domain_exception_handler(request: Request, exc: DomainException):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "error": exc.code,
                "message": exc.message
            }
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled exception: {exc}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occurred"
            }
        )