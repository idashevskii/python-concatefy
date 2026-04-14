"""
Abstract Repository Interface.
Defines the contract for data storage.
"""

from abc import ABC, abstractmethod
from todo_app.models.todo import TodoItem


class TodoRepository(ABC):
    """Abstract Base Class for Todo Storage."""

    @abstractmethod
    def add(self, item: TodoItem) -> TodoItem:
        """Save a new todo item."""
        pass

    @abstractmethod
    def get_all(self) -> list[TodoItem]:
        """Retrieve all todo items."""
        pass

    @abstractmethod
    def get_by_id(self, item_id: int) -> TodoItem | None:
        """Retrieve a specific todo item by ID."""
        pass

    @abstractmethod
    def update(self, item: TodoItem) -> None:
        """Update an existing todo item."""
        pass

    @abstractmethod
    def delete(self, item_id: int) -> None:
        """Delete a todo item."""
        pass
