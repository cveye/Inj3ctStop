# core/__init__.py
import logging
import sys
import os
from datetime import datetime

# ANSI color codes
ANSI_RESET = "\033[0m"
ANSI_BOLD = "\033[1m"
ANSI_COLORS = {
    "BLACK": "\033[30m",
    "RED": "\033[31m",
    "GREEN": "\033[32m",
    "YELLOW": "\033[33m",
    "BLUE": "\033[34m",
    "MAGENTA": "\033[35m",
    "CYAN": "\033[36m",
    "WHITE": "\033[37m",
}

LEVEL_TO_COLOR = {
    logging.DEBUG: ANSI_COLORS["CYAN"],
    logging.INFO: ANSI_COLORS["GREEN"],
    logging.WARNING: ANSI_COLORS["YELLOW"],
    logging.ERROR: ANSI_COLORS["RED"],
    logging.CRITICAL: ANSI_BOLD + ANSI_COLORS["RED"],
}


class ColoredFormatter(logging.Formatter):
    """
    Logging formatter that adds ANSI colors based on level.
    Falls back to no color if NO_COLOR env var is set or if output is not a tty.
    """

    def __init__(self, fmt=None, datefmt=None, use_color=True):
        super().__init__(fmt=fmt, datefmt=datefmt)
        # disable color if requested or not running in a TTY
        no_color_env = os.getenv("NO_COLOR", "") != ""
        self.use_color = use_color and (sys.stdout.isatty()) and (not no_color_env)

    def format(self, record):
        created = datetime.fromtimestamp(record.created).strftime(self.datefmt or "%Y-%m-%d %H:%M:%S")
        level_color = LEVEL_TO_COLOR.get(record.levelno, "")
        level_name = record.levelname
        # build prefix
        if self.use_color:
            prefix = f"{created} {level_color}[{level_name}]{ANSI_RESET} Inj3ctStop:"
        else:
            prefix = f"{created} [{level_name}] Inj3ctStop:"
        # original message formatting
        message = super().format(record)
        # remove any duplicate levelname if present in message
        # produce final string
        if self.use_color:
            return f"{prefix} {message}"
        return f"{prefix} {message}"


# Create/get logger
logger = logging.getLogger("Inj3ctStop")
# Allow the application or user to override log level via env var LOG_LEVEL
log_level_name = os.getenv("INJ3CTSTOP_LOG_LEVEL", os.getenv("LOG_LEVEL", "INFO")).upper()
try:
    logger.setLevel(getattr(logging, log_level_name))
except Exception:
    logger.setLevel(logging.INFO)

# Console handler with our colored formatter
if not logger.handlers:
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logger.level)
    formatter = ColoredFormatter(fmt="%(message)s", datefmt="%Y-%m-%d %H:%M:%S", use_color=True)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

# Exported name
__all__ = ["logger"]
