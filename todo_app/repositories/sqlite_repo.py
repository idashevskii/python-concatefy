"""
SQLite Implementation of the Todo Repository.
"""

import sqlite3 as sq
from typing import override, cast
from datetime import datetime

from todo_app.repositories.interface import TodoRepository
from todo_app.models.todo import TodoItem
from todo_app.exceptions import DatabaseError, TodoNotFoundError


class SqliteTodoRepository(TodoRepository):
    """Concrete implementation using SQLite."""

    def __init__(self, db_path: str):
        self.db_path: str = db_path
        self._init_db()

    def _get_connection(self) -> sq.Connection:
        """Get a database connection with row factory."""
        conn = sq.connect(self.db_path)
        conn.row_factory = sq.Row
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
        except sq.Error as e:
            raise DatabaseError(f"Failed to initialize database: {e}")

    def _row_to_model(self, row: sq.Row) -> TodoItem:
        """Convert a DB row to a TodoItem model."""
        return TodoItem(
            id=cast(int, row["id"]),
            title=cast(str, row["title"]),
            completed=bool(cast(str, row["completed"])),
            created_at=datetime.strptime(
                cast(str, row["created_at"]), "%Y-%m-%d %H:%M:%S.%f"
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
        except sq.Error as e:
            raise DatabaseError(f"Failed to add todo: {e}")

    @override
    def get_all(self) -> list[TodoItem]:
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                _ = cursor.execute("SELECT * FROM todos ORDER BY created_at DESC")
                return [
                    self._row_to_model(row)
                    for row in cast(list[sq.Row], cursor.fetchall())
                ]
        except sq.Error as e:
            raise DatabaseError(f"Failed to fetch todos: {e}")

    @override
    def get_by_id(self, item_id: int) -> TodoItem | None:
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                _ = cursor.execute("SELECT * FROM todos WHERE id = ?", (item_id,))
                row = cast(sq.Row, cursor.fetchone())
                return self._row_to_model(row) if row else None
        except sq.Error as e:
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
        except sq.Error as e:
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
        except sq.Error as e:
            raise DatabaseError(f"Failed to delete todo: {e}")
