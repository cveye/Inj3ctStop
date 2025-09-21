# core/__init__.py
import logging
import sys

# Create logger for the package
logger = logging.getLogger("Inj3ctStop")
logger.setLevel(logging.INFO)  # default level; can be overridden by user

# Console handler with a simple format
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)

formatter = logging.Formatter(
    fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
ch.setFormatter(formatter)

# Avoid duplicate handlers if reimported
if not logger.handlers:
    logger.addHandler(ch)

# Export logger for use in all modules
__all__ = ["logger"]
