import ast
import subprocess
from pathlib import Path


def first_function(path: str) -> ast.FunctionDef:
    tree = ast.parse(Path(path).read_text())
    return next(node for node in tree.body if isinstance(node, ast.FunctionDef))


solution_function = first_function("solution.py")
smoke_function = first_function("smoke.py")
assert ast.dump(solution_function) == ast.dump(smoke_function)

generated_mpy = subprocess.check_output(
    ["python3", "py2mpy.py", "solution.py"],
    text=True,
)
assert generated_mpy == Path("solution.mpy").read_text()

compact_mpy = "".join(generated_mpy.split())
module_prefix = 'Module(FuncDef("sum_to_n",Params("n"),'
assert compact_mpy.startswith(module_prefix)
assert compact_mpy.endswith("))")
translated_body = compact_mpy[len(module_prefix) : -2]
expected_closure = (
    'closureVal("n",.ParamNames,' + translated_body + ",0)"
)
compact_spec = "".join(Path("spec.k").read_text().split())
assert compact_spec.count(expected_closure) == 2

print(
    "function_ast_match=true "
    "solution_mpy_current=true "
    "spec_closure_matches=2"
)
