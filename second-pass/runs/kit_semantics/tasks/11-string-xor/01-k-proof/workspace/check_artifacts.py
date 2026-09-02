import ast
import re
import subprocess
import sys
from pathlib import Path


def normalized(text: str) -> str:
    return re.sub(r"\s+", "", text)


solution_source = Path("solution.py").read_text()
solution_mpy = Path("solution.mpy").read_text()
regenerated = subprocess.check_output(
    [sys.executable, "py2mpy.py", "solution.py"],
    text=True,
)
assert regenerated == solution_mpy

solution_function = ast.parse(solution_source).body[0]
concrete_function = ast.parse(Path("concrete_tests.py").read_text()).body[0]
assert ast.dump(solution_function) == ast.dump(concrete_function)

term = normalized(solution_mpy)
prefix = 'Module(FuncDef("string_xor",Params("a","b"),'
assert term.startswith(prefix) and term.endswith("))")
body = term[len(prefix):-2]
expected_closure = 'closureVal(("a","b"),' + body + ",0)"
assert expected_closure in normalized(Path("spec.k").read_text())
assert expected_closure in normalized(Path("spec-vacuity.k").read_text())

verification_text = Path("verification.k").read_text()
spec_text = Path("spec.k").read_text()
bridge = verification_text.split("  rule\n", 1)[1].split(
    "    [priority(40)]", 1
)[0]
connection_claim = spec_text.split(
    "  claim [loop-invariant]:\n", 1
)[1].split("endmodule", 1)[0]
assert normalized(bridge) == normalized(connection_claim)

print("translation_matches=true")
print("concrete_function_matches=true")
print("entry_closure_matches=true")
print("bridge_matches_connection_claim=true")
