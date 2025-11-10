"""Logging configuration for the Aircall API SDK."""

import logging
import sys
from typing import Optional


def setup_logger(
    name: str,
    level: Optional[int] = None,
    handler: Optional[logging.Handler] = None
) -> logging.Logger:
    """
    Set up a logger with consistent formatting.

    Args:
        name: Logger name (typically __name__)
        level: Logging level (defaults to WARNING if not set)
        handler: Custom handler (defaults to StreamHandler if not set)

    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(name)

    # Only configure if no handlers exist (avoid duplicate handlers)
    if not logger.handlers:
        if level is None:
            level = logging.WARNING

        logger.setLevel(level)

        if handler is None:
            handler = logging.StreamHandler(sys.stdout)

        # Create formatter with timestamp, level, and message
        formatter = logging.Formatter(
            fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


def configure_logging(level: Optional[int] = None) -> None:
    """
    Configure logging for the entire Aircall SDK.

    This sets the logging level for all Aircall loggers.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
               If None, defaults to WARNING

    Example:
        >>> import logging
        >>> from aircall.logging_config import configure_logging
        >>> configure_logging(logging.DEBUG)
    """
    if level is None:
        level = logging.WARNING

    # Configure the root aircall logger
    root_logger = logging.getLogger('aircall')
    root_logger.setLevel(level)

    # If no handlers exist on root, add a default one
    if not root_logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        root_logger.addHandler(handler)


# Create default logger for the SDK
logger = setup_logger('aircall')
