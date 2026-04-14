"""
Application Entry Point.
Wires up dependencies and starts the CLI.
"""

import argparse
import sys

from python_concatefy.process import process


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="python_concatefy",
        description="Combining python applications into a single file python script",
    )
    _ = parser.add_argument("--root", type=str, help="App Root directory")
    _ = parser.add_argument("--entry", type=str, help="Entry script relatively to root")
    _ = parser.add_argument("--dist", type=str, help="Destination file")
    _ = parser.add_argument(
        "--globals",
        type=str,
        help="Comma separated global names safe to delete",
        default="",
    )
    args = parser.parse_args()

    process(
        root_dir=args.root,  # pyright: ignore[reportAny]
        entry=args.entry,  # pyright: ignore[reportAny]
        dist=args.dist,  # pyright: ignore[reportAny]
        globals=(
            args.globals.split(",")  # pyright: ignore[reportAny]
            if args.globals  # pyright: ignore[reportAny]
            else []
        ),
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())
