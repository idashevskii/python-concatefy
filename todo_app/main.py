"""
Application Entry Point.
Wires up dependencies and starts the CLI.
"""

import sys
from todo_app.config import Config
from todo_app.repositories.sqlite_repo import SqliteTodoRepository
from todo_app.services.todo_service import TodoService
from todo_app.commands.cli import CLI
from todo_app.views.renderer import Renderer


def main() -> int:
    """
    Composition Root.
    Initializes dependencies and runs the application.
    """
    # 1. Initialize Infrastructure
    repository = SqliteTodoRepository(db_path=str(Config.DB_PATH))

    # 2. Initialize Business Logic
    service = TodoService(repository=repository)

    # 3. Initialize Presentation
    renderer = Renderer()

    # 4. Initialize CLI
    cli = CLI(service=service, renderer=renderer)

    # 5. Run
    return cli.run(sys.argv[1:])


if __name__ == "__main__":
    sys.exit(main())
