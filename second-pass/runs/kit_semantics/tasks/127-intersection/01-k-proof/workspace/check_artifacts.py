import ast
from pathlib import Path


def first_function(path):
    tree = ast.parse(Path(path).read_text(encoding="utf-8"), filename=path)
    return next(node for node in tree.body if isinstance(node, ast.FunctionDef))


solution_function = first_function("solution.py")
smoke_function = first_function("smoke.py")
mutant_function = first_function("solution-mutant.py")

assert ast.dump(solution_function) == ast.dump(smoke_function)
assert ast.dump(solution_function) != ast.dump(mutant_function)

def string_returns(function):
    nodes = [
        node
        for node in ast.walk(function)
        if isinstance(node, ast.Return)
        and isinstance(node.value, ast.Constant)
        and isinstance(node.value.value, str)
    ]
    return [node.value.value for node in sorted(nodes, key=lambda node: node.lineno)]


solution_returns = string_returns(solution_function)
mutant_returns = string_returns(mutant_function)
assert solution_returns == ["NO", "NO", "YES"]
assert mutant_returns == ["NO", "NO", "NO"]

print("artifact identity: smoke body exact; mutant changes final YES to NO")
