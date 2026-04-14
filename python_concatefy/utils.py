import ast
import pathlib


def module_to_file(name: str):
    return name.replace(".", "/") + ".py"


def file_to_module(file: str):
    return file.replace("/", ".").removesuffix(".py")


def is_docstring(node: ast.AST):
    return (
        isinstance(node, ast.Expr)
        and isinstance(node.value, ast.Constant)
        and isinstance(node.value.value, str)
    )


def optimize_lib_imports(imports: list[ast.Import | ast.ImportFrom]):
    import_base: dict[str, set[str | None]] = {}
    imports_from: dict[str, dict[str, set[str | None]]] = {}

    for imp in imports:
        if isinstance(imp, ast.Import):
            for als in imp.names:
                if als.name not in import_base:
                    import_base[als.name] = set()
                import_base[als.name].add(als.asname)
        else:
            assert imp.level == 0, "Relative modules not supported"
            module = imp.module
            assert module
            if module not in imports_from:
                imports_from[module] = {}
            als_map = imports_from[module]
            for als in imp.names:
                if als.name not in als_map:
                    als_map[als.name] = set()
                als_map[als.name].add(als.asname)

    result_imports: list[ast.Import | ast.ImportFrom] = []
    for module, aliases in import_base.items():
        for as_name in aliases:
            result_imports.append(
                ast.Import(names=[ast.alias(name=module, asname=as_name)])
            )

    for module, item_to_aliases in imports_from.items():
        imported_items: list[ast.alias] = []
        for item, aliases in item_to_aliases.items():
            for as_name in aliases:
                imported_items.append(ast.alias(item, asname=as_name))
        result_imports.append(
            ast.ImportFrom(module=module, names=imported_items, level=0)
        )

    return result_imports


class AstManager:
    def __init__(self, root_dir: str) -> None:
        self.root_dir: str = root_dir

    def _make_full_path(self, file: str) -> pathlib.Path:
        return pathlib.Path(f"{self.root_dir}/{file}")

    def is_module(self, name: str):
        return self._make_full_path(module_to_file(name)).exists()

    def read_module(self, name: str):
        return self.read(module_to_file(name))

    def read(self, file: str):
        # 1. Read the script file
        with open(self._make_full_path(file), "r") as f:
            source_code = f.read()
            tree = ast.parse(source_code)
        return tree

    def write(self, tree: ast.Module, file: str):
        with open(self._make_full_path(file), "w") as f:
            _ = f.write(ast.unparse(tree))
