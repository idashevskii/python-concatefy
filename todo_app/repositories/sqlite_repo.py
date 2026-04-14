"""
SQLite Implementation of the Todo Repository.
"""

import sqlite3
from typing import override
from datetime import datetime

from todo_app.repositories.interface import TodoRepository
from todo_app.models.todo import TodoItem
from todo_app.exceptions import DatabaseError, TodoNotFoundError


class SqliteTodoRepository(TodoRepository):
    """Concrete implementation using SQLite."""

    def __init__(self, db_path: str):
        self.db_path: str = db_path
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        """Get a database connection with row factory."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        """Initialize the database schema."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                _ = cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS todos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        completed INTEGER DEFAULT 0,
                        created_at TEXT NOT NULL
                    )
                """
                )
                conn.commit()
        except sqlite3.Error as e:
            raise DatabaseError(f"Failed to initialize database: {e}")

    def _row_to_model(self, row: sqlite3.Row) -> TodoItem:
        """Convert a DB row to a TodoItem model."""
        return TodoItem(
            id=row["id"],  # pyright: ignore[reportAny]
            title=row["title"],  # pyright: ignore[reportAny]
            completed=bool(row["completed"]),  # pyright: ignore[reportAny]
            created_at=datetime.strptime(
                row["created_at"], "%Y-%m-%d %H:%M:%S.%f"  # pyright: ignore[reportAny]
            ),
        )

    @override
    def add(self, item: TodoItem) -> TodoItem:
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                _ = cursor.execute(
                    "INSERT INTO todos (title, completed, created_at) VALUES (?, ?, ?)",
                    (
                        item.title,
                        int(item.completed),
                        item.created_at.strftime("%Y-%m-%d %H:%M:%S.%f"),
                    ),
                )
                conn.commit()
                item.id = cursor.lastrowid
                return item
        except sqlite3.Error as e:
            raise DatabaseError(f"Failed to add todo: {e}")

    @override
    def get_all(self) -> list[TodoItem]:
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                _ = cursor.execute("SELECT * FROM todos ORDER BY created_at DESC")
                return [
                    self._row_to_model(row)  # pyright: ignore[reportAny]
                    for row in cursor.fetchall()  # pyright: ignore[reportAny]
                ]
        except sqlite3.Error as e:
            raise DatabaseError(f"Failed to fetch todos: {e}")

    @override
    def get_by_id(self, item_id: int) -> TodoItem | None:
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                _ = cursor.execute("SELECT * FROM todos WHERE id = ?", (item_id,))
                row = cursor.fetchone()  # pyright: ignore[reportAny]
                return (
                    self._row_to_model(row)  # pyright: ignore[reportAny]
                    if row
                    else None
                )
        except sqlite3.Error as e:
            raise DatabaseError(f"Failed to fetch todo: {e}")

    @override
    def update(self, item: TodoItem) -> None:
        if item.id is None:
            raise TodoNotFoundError("Cannot update item without ID")

        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                _ = cursor.execute(
                    "UPDATE todos SET title = ?, completed = ? WHERE id = ?",
                    (item.title, int(item.completed), item.id),
                )
                if cursor.rowcount == 0:
                    raise TodoNotFoundError(f"Todo with ID {item.id} not found")
                conn.commit()
        except sqlite3.Error as e:
            raise DatabaseError(f"Failed to update todo: {e}")

    @override
    def delete(self, item_id: int) -> None:
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                _ = cursor.execute("DELETE FROM todos WHERE id = ?", (item_id,))
                if cursor.rowcount == 0:
                    raise TodoNotFoundError(f"Todo with ID {item_id} not found")
                conn.commit()
        except sqlite3.Error as e:
            raise DatabaseError(f"Failed to delete todo: {e}")
