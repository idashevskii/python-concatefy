"""
Business Logic Layer.
Orchestrates data flow between commands and repositories.
"""

from todo_app.models.todo import TodoItem
from todo_app.repositories.interface import TodoRepository
from todo_app.exceptions import TodoNotFoundError


class TodoService:
    """Handles business logic for Todo items."""

    def __init__(self, repository: TodoRepository):
        self.repo: TodoRepository = repository

    def create_todo(self, title: str) -> TodoItem:
        if not title.strip():
            raise ValueError("Title cannot be empty")
        item = TodoItem(title=title)
        return self.repo.add(item)

    def list_todos(self, show_completed: bool = True) -> list[TodoItem]:
        all_items = self.repo.get_all()
        if not show_completed:
            return [item for item in all_items if not item.completed]
        return all_items

    def complete_todo(self, item_id: int) -> TodoItem:
        item = self.repo.get_by_id(item_id)
        if not item:
            raise TodoNotFoundError(f"Todo with ID {item_id} not found")

        item.completed = True
        self.repo.update(item)
        return item

    def delete_todo(self, item_id: int) -> None:
        self.repo.delete(item_id)
