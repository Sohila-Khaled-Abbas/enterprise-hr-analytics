"""
Standardized Enterprise Logging Module.
Provides uniform structured logging with clean timestamping and Windows UTF-8 console support.
"""

import logging
import sys
from functools import lru_cache
from typing import Optional


# Ensure UTF-8 output on Windows terminal
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


class ColorFormatter(logging.Formatter):
    """Custom colorized formatter for developer consoles."""
    COLORS = {
        logging.DEBUG: "\033[36m",    # Cyan
        logging.INFO: "\033[32m",     # Green
        logging.WARNING: "\033[33m",  # Yellow
        logging.ERROR: "\033[31m",    # Red
        logging.CRITICAL: "\033[35m", # Magenta
    }
    RESET = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        color = self.COLORS.get(record.levelno, self.RESET)
        record.levelname = f"{color}{record.levelname:<8}{self.RESET}"
        return super().format(record)


@lru_cache(maxsize=32)
def get_logger(name: str = "EnterpriseHR", level: Optional[str] = None) -> logging.Logger:
    """
    Creates and returns a standardized logger instance.

    Args:
        name: Name of the logger component
        level: Optional log level override (e.g. 'DEBUG', 'INFO')

    Returns:
        Configured logging.Logger
    """
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    log_level = getattr(logging, (level or "INFO").upper(), logging.INFO)
    logger.setLevel(log_level)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(log_level)

    formatter = logging.Formatter(
        fmt="%(asctime)s │ %(levelname)-8s │ %(name)s │ %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False

    return logger
