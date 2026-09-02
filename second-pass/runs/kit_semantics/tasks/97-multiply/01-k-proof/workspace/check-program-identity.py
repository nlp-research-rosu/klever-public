import ast
from pathlib import Path


source = Path("solution.py").read_text()
tree = ast.parse(source)
assert len(tree.body) == 1
function = tree.body[0]
assert isinstance(function, ast.FunctionDef)
assert function.name == "multiply"
assert [argument.arg for argument in function.args.args] == ["a", "b"]
assert len(function.body) == 1
assert isinstance(function.body[0], ast.Return)

expected = ast.parse(
    "def multiply(a, b):\n"
    "    return (a % 10) * (b % 10)\n"
).body[0]
assert ast.dump(function, include_attributes=False) == ast.dump(
    expected, include_attributes=False
)

body_term = (
    'Return(BinOp("*",BinOp("%",Name("a"),Int(10)),'
    'BinOp("%",Name("b"),Int(10))))'
)
solution_term = "".join(Path("solution.mpy").read_text().split())
spec_term = "".join(Path("spec.k").read_text().split())
assert body_term in solution_term
assert body_term in spec_term

print("PROGRAM IDENTITY: PASS")
