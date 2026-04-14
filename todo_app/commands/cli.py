"""
Command Line Interface Definition.
Parses arguments and dispatches to services.
"""

import argparse
import logging

from todo_app.services.todo_service import TodoService
from todo_app.views.renderer import Renderer
from todo_app.exceptions import TodoError, TodoNotFoundError

logger = logging.getLogger(__name__)


class CLI:
    """Main CLI Handler."""

    def __init__(self, service: TodoService, renderer: Renderer):
        self.service: TodoService = service
        self.renderer: Renderer = renderer

    def create_parser(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(
            prog="todo", description="A simple command line todo manager."
        )
        subparsers = parser.add_subparsers(dest="command", help="Available commands")

        # Add Command
        parser_add = subparsers.add_parser("add", help="Add a new todo")
        _ = parser_add.add_argument("title", type=str, help="The title of the todo")

        # List Command
        parser_list = subparsers.add_parser("list", help="List todos")
        _ = parser_list.add_argument(
            "--pending", action="store_true", help="Show only pending todos"
        )

        # Done Command
        parser_done = subparsers.add_parser("done", help="Mark a todo as completed")
        _ = parser_done.add_argument("id", type=int, help="The ID of the todo")

        # Delete Command
        parser_delete = subparsers.add_parser("delete", help="Delete a todo")
        _ = parser_delete.add_argument("id", type=int, help="The ID of the todo")

        return parser

    def run(self, args: list[str] | None = None) -> int:
        parser = self.create_parser()
        parsed_args = parser.parse_args(args)

        if not parsed_args.command:  # pyright: ignore[reportAny]
            parser.print_help()
            return 0

        try:
            if parsed_args.command == "add":  # pyright: ignore[reportAny]
                item = self.service.create_todo(
                    parsed_args.title  # pyright: ignore[reportAny]
                )
                self.renderer.print_success(f"Added todo #{item.id}: {item.title}")

            elif parsed_args.command == "list":  # pyright: ignore[reportAny]
                items = self.service.list_todos(
                    show_completed=not parsed_args.pending  # pyright: ignore[reportAny]
                )
                self.renderer.print_todos(items)

            elif parsed_args.command == "done":  # pyright: ignore[reportAny]
                item = self.service.complete_todo(
                    parsed_args.id  # pyright: ignore[reportAny]
                )
                self.renderer.print_success(f"Marked todo #{item.id} as completed")

            elif parsed_args.command == "delete":  # pyright: ignore[reportAny]
                self.service.delete_todo(parsed_args.id)  # pyright: ignore[reportAny]
                self.renderer.print_success(
                    f"Deleted todo #{parsed_args.id}"  # pyright: ignore[reportAny]
                )

            return 0

        except TodoNotFoundError as e:
            self.renderer.print_error(str(e))
            return 1
        except ValueError as e:
            self.renderer.print_error(str(e))
            return 1
        except TodoError as e:
            self.renderer.print_error(str(e))
            return 1
        except Exception as e:
            self.renderer.print_error(f"Unexpected error: {e}")
            return 1
