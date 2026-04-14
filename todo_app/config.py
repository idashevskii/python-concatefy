"""
Application configuration settings.
"""

from pathlib import Path


class Config:
    """Holds application constants and settings."""

    # Database file location (in user's home dir or local)
    DB_PATH: Path = Path.cwd() / "dist" / "todos.db"

    # Date format for display
    DATE_FORMAT: str = "%Y-%m-%d %H:%M"
