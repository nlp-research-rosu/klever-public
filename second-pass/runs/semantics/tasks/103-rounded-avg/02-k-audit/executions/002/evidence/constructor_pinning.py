#!/usr/bin/env python3
"""Mechanically compare solution.mpy's function body with verification.k's RHS."""

import hashlib
import json
from pathlib import Path
import subprocess


WORK = Path("/tmp/audit-work/103-rounded-avg")
DEFINITION = WORK / "audit-verification-kompiled"


def kast(path: Path, sort: str):
    output = subprocess.check_output(
        [
            "kast",
            str(path),
            "--definition",
            str(DEFINITION),
            "--sort",
            sort,
            "--output",
            "json",
        ],
        cwd=WORK,
        text=True,
    )
    return json.loads(output)["term"]


module_term = kast(WORK / "solution.mpy", "Module")
module_stmts = module_term["args"][0]
function_def = module_stmts["args"][0]
if not function_def["label"]["name"].startswith("FuncDef(_,_,_)"):
    raise RuntimeError("solution.mpy does not begin with the expected FuncDef")
solution_body = function_def["args"][2]

lines = (WORK / "verification.k").read_text(encoding="utf-8").splitlines()
start = lines.index("  rule roundedAvgBody")
rhs_lines = []
for line in lines[start + 1 :]:
    if line.startswith("  // A direct entry-point call."):
        break
    if not rhs_lines and "=>" in line:
        rhs_lines.append(line.split("=>", 1)[1])
    elif rhs_lines:
        rhs_lines.append(line)
while rhs_lines and not rhs_lines[-1].strip():
    rhs_lines.pop()
term_path = WORK / "audit-rounded-body.term"
# The program parser spells empty K List productions as an empty field, while
# rule syntax may use their generated unit labels explicitly.
program_syntax_rhs = (
    "\n".join(rhs_lines)
    .replace(", .Exprs", "")
    .replace(".Stmts", "")
    .replace(".Exprs", "")
)
term_path.write_text(program_syntax_rhs + "\n", encoding="utf-8")
verification_body = kast(term_path, "Stmts")


def digest(term) -> str:
    encoded = json.dumps(term, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


print("solution_body_sha256=" + digest(solution_body))
print("verification_rhs_sha256=" + digest(verification_body))
print("constructor_terms_equal=" + str(solution_body == verification_body))
print("extracted_verification_term=" + str(term_path))
if solution_body != verification_body:
    raise SystemExit(1)
