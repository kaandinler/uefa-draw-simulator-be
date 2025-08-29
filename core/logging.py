import logging
import sys
from loguru import logger
from core.config import settings


class InterceptHandler(logging.Handler):
    """Intercept standard logging messages and forward to loguru"""

    def emit(self, record: logging.LogRecord) -> None:
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def setup_logging() -> None:
    """Configure logging for the application"""

    # Remove default handlers
    logging.root.handlers = [InterceptHandler()]
    logging.root.setLevel(settings.LOG_LEVEL)

    # Remove default loguru handler
    logger.remove()

    # Add custom loguru handler
    logger.add(
        sys.stderr,
        format=settings.LOG_FORMAT,
        level=settings.LOG_LEVEL,
        backtrace=settings.DEBUG,
        diagnose=settings.DEBUG,
    )

    # Add file handler for production
    if not settings.DEBUG:
        logger.add(
            "logs/uefa_draw_{time}.log",
            rotation="500 MB",
            retention="10 days",
            level="INFO",
            format=settings.LOG_FORMAT,
        )

    # Configure loggers for libraries
    for logger_name in ("uvicorn", "uvicorn.access", "sqlalchemy.engine"):
        logging.getLogger(logger_name).handlers = [InterceptHandler()]