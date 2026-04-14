from python_concatefy.concatenator import Concatenator
from python_concatefy.utils import AstManager, file_to_module
from python_concatefy.validator import validate


def process(
    root_dir: str,
    entry: str,
    dist: str,
    globals: list[str],
):
    am = AstManager(root_dir=root_dir)

    cc = Concatenator(am=am, globals=globals)
    tree = cc.concat(file_to_module(entry))

    tree = validate(tree, known_globals=set(globals))

    am.write(tree, dist)
