# Logging middleware
import time
import uuid
from fastapi import FastAPI, Request
from loguru import logger


def setup_logging_middleware(app: FastAPI) -> None:
    """Configure logging middleware"""

    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        request_id = str(uuid.uuid4())
        start_time = time.time()

        # Add request ID to request state
        request.state.request_id = request_id

        # Log request
        logger.info(
            f"Request started - ID: {request_id}, "
            f"Method: {request.method}, "
            f"Path: {request.url.path}"
        )

        # Process request
        response = await call_next(request)

        # Calculate process time
        process_time = time.time() - start_time

        # Add headers
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = str(process_time)

        # Log response
        logger.info(
            f"Request completed - ID: {request_id}, "
            f"Status: {response.status_code}, "
            f"Time: {process_time:.3f}s"
        )

        return response