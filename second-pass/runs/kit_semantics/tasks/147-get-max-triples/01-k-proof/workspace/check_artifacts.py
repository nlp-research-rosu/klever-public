import ast
import re


def normalized(path):
    with open(path, encoding="utf-8") as stream:
        return re.sub(r"\s+", "", stream.read())


def only_function(path):
    with open(path, encoding="utf-8") as stream:
        tree = ast.parse(stream.read(), filename=path)
    functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)]
    assert len(functions) == 1
    return ast.dump(functions[0], include_attributes=False)


solution_term = normalized("solution.mpy")
prefix = 'Module(FuncDef("get_max_triples",Params("n"),'
assert solution_term.startswith(prefix)
assert solution_term.endswith("))")
body = solution_term[len(prefix):-2]

spec_term = normalized("spec.k")
assert f'closureVal("n",{body},0)' in spec_term
assert only_function("solution.py") == only_function("smoke.py")

print(
    "artifact-identity=PASS; "
    "solution.mpy body equals spec.k closure body and smoke.py function AST"
)
