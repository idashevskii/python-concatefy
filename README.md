Combining python applications into a single file python script

## Usage example
```bash
python -m src.python_concatefy.main --root . --entry todo_app/main.py --dist ./dist/todo.py
```


## Demo App for concatenation
Run:
```bash
python -m todo_app.main
```

## Restrictions
- All global names must be unique. There could be explicitly specified exceptions, which will be dropped (e.g. `logger`)
- `__all__` is not supported.
