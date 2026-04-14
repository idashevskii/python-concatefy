"""
Presentation Layer.
Handles formatting and printing to the console.
"""

import logging
import sys
from todo_app.models.todo import TodoItem
from todo_app.config import Config

logger = logging.getLogger(__name__)


class Renderer:
    """Formats and outputs data to the terminal."""

    @staticmethod
    def print_success(message: str) -> None:
        print(f"✓ {message}")

    @staticmethod
    def print_error(message: str) -> None:
        print(f"✗ Error: {message}", file=sys.stderr)

    @staticmethod
    def print_todos(items: list[TodoItem]) -> None:
        if not items:
            print("No todos found.")
            return

        print(f"{'ID':<5} {'Status':<8} {'Title':<30} {'Created':<20}")
        print("-" * 65)

        for item in items:
            status = "Done" if item.completed else "Pending"
            created = item.created_at.strftime(Config.DATE_FORMAT)
            # Truncate title if too long
            title = (item.title[:27] + "...") if len(item.title) > 30 else item.title
            print(f"{item.id:<5} {status:<8} {title:<30} {created:<20}")

    @staticmethod
    def print_todo(item: TodoItem | None) -> None:
        if item:
            print(f"Details for ID {item.id}:")
            print(f"  Title: {item.title}")
            print(f"  Status: {'Completed' if item.completed else 'Pending'}")
            print(f"  Created: {item.created_at.strftime(Config.DATE_FORMAT)}")
        else:
            print("Todo not found.")
