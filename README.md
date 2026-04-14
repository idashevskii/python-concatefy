# Python Concatefy

[![Python Version](https://img.shields.io/badge/python-3.14+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-black-black.svg)](https://github.com/psf/black)

**Combine multiple Python application files into a single executable script.**

Python Concatefy is a lightweight bundler designed to merge a multi-file Python project into a single `.py` file. This is useful for distributing simple tools, submitting coding challenges with file limits, or creating portable scripts without external dependencies.

## 🚀 Features

- **Single File Output**: Merges your entire project logic into one portable script.
- **Configurable Entry Point**: Specify exactly which file serves as the application entry.
- **Dependency Free**: The resulting script requires only the standard Python interpreter to run.
- **Simple CLI**: Easy-to-use command-line interface for quick bundling.

## 📦 Installation

Currently, Python Concatefy is available via source.

### Clone and Run
```bash
git clone https://github.com/idashevskii/python-concatefy.git
cd python_concatefy
```

## 💻 Usage

To concatenate your project files, run the module from the root of your project.

### Basic Command
```bash
python -m python_concatefy.main --root ./target/root --entry ./entry.py --dist ./dist/app.py --globals logger
```

### CLI Arguments

| Argument    | Description                                            | Example                   |
| :---------- | :----------------------------------------------------- | :------------------------ |
| `--root`    | The root directory of the source project.              | `.` or `/path/to/project` |
| `--entry`   | The relative path to the main entry file.              | `todo_app/main.py`        |
| `--dist`    | The destination path for the concatenated output file. | `./dist/todo.py`          |
| `--globals` | Comma separated global names safe to delete.           | `logger`                  |

## 🧪 Demo App

This repository includes a sample application (`todo_app`) to test the concatenation process.

### 1. Run the Original Demo App
Before concatenation, verify the demo app works as expected:
```bash
python -m todo_app.main
```

### 2. Concatenate the Demo App
Bundle the demo app into a single file:
```bash
python -m python_concatefy.main --root . --entry todo_app/main.py --dist ./dist/todo.py --globals logger
```

### 3. Run the Bundled App
Execute the newly created single-file script:
```bash
python ./dist/todo.py
```

## ⚠️ Restrictions & Limitations

Due to the nature of concatenating files into a single namespace, please adhere to the following constraints:

1.  **Unique Global Names**: All global variables, functions, and class names across all files must be unique.
    *   *Reason*: Files are merged into a single scope.
    *   *Exception*: You can specify explicit exceptions to be dropped during merging (e.g., `logger` instances).
2.  **Import Handling**: Relative imports are resolved based on the `--root` path. Circular imports may cause issues.
3.  **__all__**: The `__all__` variable is ignored during concatenation.
    *   *Impact*: You cannot control `from module import *` behavior in the output.
4.  **Local Imports**: Only global (top level) imports are supported.
5.  **Import Aliases**: Constructions like `import ... as ...` are not supported.
6.  **Module Docstrings**: Module Docstrings are removed from result file
7.  **Comments**: All comments are stripped.
8.  **Dot Imports**: Relative imports using dots are not supported.

## 🛠 Development

### Project Structure
```text
.
├── 
│   python_concatefy/
│   └── main.py           # Tool entry point
├── todo_app/             # Demo application
│   └── main.py
├── tests/                # Test cases
├── dist/                 # Output directory (gitignored)
└── README.md
```

### Running Tests
```bash
python -m unittest  discover -s ./tests -p test_*.py
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1.  Fork the repository.
2.  Create a feature branch (`git checkout -b feature/amazing-feature`).
3.  Commit your changes (`git commit -m 'Add some amazing feature'`).
4.  Push to the branch (`git push origin feature/amazing-feature`).
5.  Open a Pull Request.

## 📄 License

This project is licensed under the [MIT License](LICENSE).
