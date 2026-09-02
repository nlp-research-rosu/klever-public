#!/usr/bin/env python3
"""Compare submitted FuncDef with the claim's macro after K macro expansion."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

work = Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/audit-work/minpath-129")
definition_name = sys.argv[2] if len(sys.argv) > 2 else "verification-audit-kompiled"
module_name = sys.argv[3] if len(sys.argv) > 3 else "VERIFICATION"
expectation = sys.argv[4] if len(sys.argv) > 4 else "equal"
source = (work / "solution.mpy").read_text()
start = source.index('FuncDef("minPath"')
depth = 0
quoted = False
escaped = False
end = None
for index in range(start, len(source)):
    char = source[index]
    if quoted:
        if escaped:
            escaped = False
        elif char == "\\":
            escaped = True
        elif char == '"':
            quoted = False
        continue
    if char == '"':
        quoted = True
    elif char == '(':
        depth += 1
    elif char == ')':
        depth -= 1
        if depth == 0:
            end = index + 1
            break
if end is None:
    raise RuntimeError("unterminated FuncDef")

submitted = source[start:end]
claim_term = 'FuncDef("minPath", Params("grid", "k"), minPathBody)'

def kast(term):
    proc = subprocess.run([
        "kast", "--definition", str(work / definition_name),
        "--module", module_name, "--sort", "Stmt", "--expression", term,
        "--expand-macros", "--output", "json",
    ], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f"kast_exit={proc.returncode}")
    if proc.stderr:
        print("kast_stderr=" + proc.stderr.strip().replace("\n", "\\n"))
    if proc.returncode:
        raise RuntimeError("kast failed")
    return json.loads(proc.stdout)["term"]

submitted_ast = kast(submitted)
claim_ast = kast(claim_term)
submitted_json = json.dumps(submitted_ast, sort_keys=True, separators=(",", ":")).encode()
claim_json = json.dumps(claim_ast, sort_keys=True, separators=(",", ":")).encode()
print(f"submitted_funcdef_chars={len(submitted)}")
print(f"submitted_constructor_sha256={hashlib.sha256(submitted_json).hexdigest()}")
print(f"claim_constructor_sha256={hashlib.sha256(claim_json).hexdigest()}")
print(f"constructor_equal={submitted_ast == claim_ast}")
expected_equal = expectation == "equal"
print(f"expected_equal={expected_equal}")
sys.exit(0 if (submitted_ast == claim_ast) == expected_equal else 1)
