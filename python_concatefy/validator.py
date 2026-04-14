import ast
from typing import override

IGNORED_GLOBAL_NAMES = set(["_"])


def validate(tree: ast.Module, known_globals: set[str]):
    global_names: set[str] = set()

    def add_global_name[T: ast.AST](node: T, names: list[str]) -> T | None:
        for name in names:
            if name in IGNORED_GLOBAL_NAMES:
                continue
            if name not in global_names:
                global_names.add(name)
            elif name in known_globals:
                return None  # ignore node as valid dupliate
            else:
                raise ValueError(
                    f"Key '{name}' must be globally unique or add it to globals list to ignore"
                )
        return node

    class ValidateModule(ast.NodeTransformer):
        @override
        def visit_FunctionDef(self, node: ast.FunctionDef):
            return add_global_name(node, names=[node.name])

        @override
        def visit_ClassDef(self, node: ast.ClassDef):
            return add_global_name(node, names=[node.name])

        @override
        def visit_Assign(self, node: ast.Assign):
            names: list[str] = []
            for t in node.targets:
                if isinstance(t, ast.Name):
                    names.append(t.id)

            return add_global_name(node, names=names)

    ValidateModule().visit(tree)

    return tree
