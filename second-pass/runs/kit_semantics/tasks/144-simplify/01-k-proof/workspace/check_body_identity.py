import ast
import re
import symtable

import py2mpy


source = open("solution.py", encoding="utf-8").read()
tree = ast.parse(source, filename="solution.py")
py2mpy.SCOPES.clear()
py2mpy._walk_symtable(symtable.symtable(source, "solution.py", "exec"))

rendered_module = py2mpy.render(py2mpy.emit_module(tree)) + "\n"
stored_module = open("solution.mpy", encoding="utf-8").read()
module_matches = rendered_module == stored_module

function_node = py2mpy.emit_stmt(tree.body[0])
rendered_body = py2mpy.render(function_node.args[-1])
verification = open("verification.k", encoding="utf-8").read()

loop_body = re.search(
    r"  rule simplifyLoopBody =>\n(.*?)\n\n  rule simplifyReturn =>",
    verification,
    re.S,
).group(1)
return_stmt = re.search(
    r"  rule simplifyReturn =>\n(.*?)\n\n  rule simplifyBody =>",
    verification,
    re.S,
).group(1)
proof_body = re.search(
    r"  rule simplifyBody =>\n(.*?)\n\n  rule simplifyScope",
    verification,
    re.S,
).group(1)
proof_body = proof_body.replace("simplifyLoopBody", loop_body)
proof_body = proof_body.replace("simplifyReturn", return_stmt)


def normalize(term):
    term = re.sub(r"\s+", "", term)
    return term.replace(",.Exprs", "").replace(".Stmts", "")


body_matches = normalize(rendered_body) == normalize(proof_body)
print(
    f"solution_mpy_matches={module_matches} "
    f"proof_body_matches={body_matches}"
)
if not module_matches or not body_matches:
    raise AssertionError("translated program and verification body differ")
