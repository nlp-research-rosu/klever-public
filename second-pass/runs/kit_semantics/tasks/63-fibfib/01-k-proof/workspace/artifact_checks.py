import ast
import re
from pathlib import Path


def normalized_k(path: str) -> str:
    text = re.sub(r"\s+", "", Path(path).read_text())
    # K's Stmts list terminator is optional in parsed surface syntax.  The
    # translator omits it while the hand-written claim spells it explicitly.
    return text.replace(".Stmts", "")


solution_tree = ast.parse(Path("solution.py").read_text())
harness_tree = ast.parse(Path("concrete_test.py").read_text())
solution_function = solution_tree.body[0]
harness_function = harness_tree.body[0]

assert isinstance(solution_function, ast.FunctionDef)
assert solution_function.name == "fibfib"
assert [arg.arg for arg in solution_function.args.args] == ["n"]
assert ast.dump(solution_function, include_attributes=False) == ast.dump(
    harness_function, include_attributes=False
)
assert normalized_k("solution.mpy") in normalized_k("spec.k")

print("entry-point: fibfib(n)")
print("concrete-harness-body: identical")
print("solution.mpy-in-entry-claim: yes")
