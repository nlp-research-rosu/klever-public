import ast
from pathlib import Path

from solution import decimal_to_binary


def function_ast(path):
    tree = ast.parse(Path(path).read_text(encoding="utf-8"), filename=path)
    return ast.dump(next(node for node in tree.body
                         if isinstance(node, ast.FunctionDef)
                         and node.name == "decimal_to_binary"))


assert function_ast("solution.py") == function_ast("smoke.py")

checked = list(range(0, 10001))
checked += [2 ** exponent - 1 for exponent in range(1, 257)]
checked += [2 ** exponent for exponent in range(1, 257)]
checked += [2 ** exponent + 1 for exponent in range(1, 257)]

for value in checked:
    expected = "db" + format(value, "b") + "db"
    actual = decimal_to_binary(value)
    assert actual == expected, (value, actual, expected)

print(f"CPython differential: {len(checked)} cases, 0 mismatches")
