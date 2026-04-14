import ast
from python_concatefy.utils import (
    AstManager,
    is_docstring,
    optimize_lib_imports,
)


class Concatenator:
    def __init__(
        self,
        am: AstManager,
        globals: list[str],
    ) -> None:
        self.lib_imports: list[ast.Import | ast.ImportFrom] = []
        self.app_imported: set[str] = set()

        self.globals: list[str] = globals
        self.processed: set[str] = set()
        self.am: AstManager = am

    def concat(self, name: str):
        tree = self.import_module(name)
        assert tree

        lib_imports = optimize_lib_imports(self.lib_imports)
        tree.body = lib_imports + tree.body

        return tree

    def import_module(self, name: str):
        if name in self.app_imported:
            return
        self.app_imported.add(name)

        am = self.am
        tree = am.read_module(name)
        # print(ast.dump(tree, indent=4))
        new_body: list[ast.stmt] = []

        def insert_module(name: str):
            ins_tree = self.import_module(name)
            if not ins_tree:
                # print(f"Module {name}: skipped")
                return
            # print(f"Module {name}: inserted")
            new_body.extend(ins_tree.body)

        for node in tree.body:
            if is_docstring(node):
                continue
            if isinstance(node, ast.Import):
                for als in node.names:
                    if am.is_module(als.name):
                        insert_module(als.name)
                    else:
                        self.lib_imports.append(ast.Import([als]))
                continue
            elif isinstance(node, ast.ImportFrom):
                if node.module and am.is_module(node.module):
                    insert_module(node.module)
                else:
                    self.lib_imports.append(node)
                continue
            new_body.append(node)
        tree.body = new_body
        return tree
