"""
Custom exceptions for the Todo application.
"""


class TodoError(Exception):
    """Base exception for Todo app errors."""

    pass


class TodoNotFoundError(TodoError):
    """Raised when a specific todo item is not found."""

    pass


class DatabaseError(TodoError):
    """Raised when database operations fail."""

    pass
