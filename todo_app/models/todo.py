"""
Data models for the Todo application.
"""

from dataclasses import dataclass, field
from datetime import datetime
import logging
from typing import override

logger = logging.getLogger(__name__)


@dataclass
class TodoItem:
    """Represents a single Todo item."""

    title: str
    id: int | None = None
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)

    @override
    def __str__(self) -> str:
        status = "✓" if self.completed else "○"
        return f"[{status}] {self.title}"
