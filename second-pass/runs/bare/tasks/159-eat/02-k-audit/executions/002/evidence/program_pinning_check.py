#!/usr/bin/env python3
"""Mechanically compare solution.mpy with the solutionProgram rule RHS."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path


REBUILD = Path("/tmp/audit-work/159-eat-audit/rebuild")
verification_path = REBUILD / "verification.k"
submitted_path = REBUILD / "solution.mpy"
extracted_path = REBUILD / "extracted-solution-program.mpy"

source = verification_path.read_text(encoding="utf-8")
match = re.search(r"\brule\s+solutionProgram\s*=>\s*", source)
if match is None:
    raise RuntimeError("solutionProgram rule not found")

start = match.end()
while start < len(source) and source[start].isspace():
    start += 1
if not source.startswith("Module(", start):
    raise RuntimeError(f"unexpected solutionProgram RHS near {source[start:start+40]!r}")

depth = 0
in_string = False
escaped = False
end = None
for index in range(start, len(source)):
    char = source[index]
    if in_string:
        if escaped:
            escaped = False
        elif char == "\\":
            escaped = True
        elif char == '"':
            in_string = False
        continue
    if char == '"':
        in_string = True
    elif char == "(":
        depth += 1
    elif char == ")":
        depth -= 1
        if depth == 0:
            end = index + 1
            break

if end is None:
    raise RuntimeError("unterminated solutionProgram RHS")

rhs = source[start:end]
suffix = source[end:]
if not re.fullmatch(r"\s*endmodule\s*", suffix):
    raise RuntimeError(f"unexpected text after solutionProgram RHS: {suffix!r}")
# Rule syntax writes the empty Stmts list as `.Stmts`; the concrete program
# grammar represents that same list identity by zero Stmt items. Perform only
# this constructor-list identity normalization before invoking the program
# parser.
if rhs.count(".Stmts") != 1:
    raise RuntimeError(f"expected exactly one .Stmts identity, got {rhs.count('.Stmts')}")
concrete_rhs = rhs.replace(".Stmts", "")
extracted_path.write_text(concrete_rhs + "\n", encoding="utf-8")


def kast_json(path: Path) -> tuple[int, str, str]:
    command = [
        "/usr/bin/kast",
        str(path),
        "--definition",
        str(REBUILD / "proof-kompiled"),
        "--module",
        "VERIFICATION",
        "--sort",
        "Pgm",
        "--output",
        "json",
    ]
    completed = subprocess.run(
        command,
        cwd=REBUILD,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    return completed.returncode, completed.stdout, completed.stderr


submitted_status, submitted_json, submitted_error = kast_json(submitted_path)
extracted_status, extracted_json, extracted_error = kast_json(extracted_path)
if submitted_error:
    print(f"submitted_stderr={submitted_error}")
if extracted_error:
    print(f"extracted_stderr={extracted_error}")

submitted_ast = json.loads(submitted_json) if submitted_status == 0 else None
extracted_ast = json.loads(extracted_json) if extracted_status == 0 else None
same = submitted_ast == extracted_ast and submitted_ast is not None

print(f"verification={verification_path}")
print(f"submitted={submitted_path}")
print(f"extracted={extracted_path}")
print(f"extracted_rhs={rhs}")
print("normalization=.Stmts rule identity -> empty concrete Stmts sequence")
print(f"submitted_kast_exit={submitted_status}")
print(f"extracted_kast_exit={extracted_status}")
print(
    "submitted_kast_sha256="
    + hashlib.sha256(submitted_json.encode()).hexdigest()
)
print(
    "extracted_kast_sha256="
    + hashlib.sha256(extracted_json.encode()).hexdigest()
)
print(f"constructor_ast_equal={same}")
sys.exit(0 if same else 1)
