import ast
import re
from pathlib import Path


def first_function(path):
    module = ast.parse(Path(path).read_text(encoding="utf-8"))
    return next(node for node in module.body if isinstance(node, ast.FunctionDef))


solution_function = ast.dump(
    first_function("solution.py"), include_attributes=False
)
smoke_function = ast.dump(first_function("smoke.py"), include_attributes=False)
assert solution_function == smoke_function

verification = Path("verification.k").read_text(encoding="utf-8")
start_marker = "  rule triangleProgram() =>\n"
end_marker = "\n\n  // Contract-level summaries."
start = verification.index(start_marker) + len(start_marker)
end = verification.index(end_marker, start)
quoted_program = verification[start:end]

solution_mpy = Path("solution.mpy").read_text(encoding="utf-8")
compact_quote = re.sub(r"\s+", "", quoted_program).replace(".Stmts)", ")")
compact_mpy = re.sub(r"\s+", "", solution_mpy)
assert compact_quote == compact_mpy

print("Artifact identity checks passed: solution/smoke AST and solution.mpy/K quote")
