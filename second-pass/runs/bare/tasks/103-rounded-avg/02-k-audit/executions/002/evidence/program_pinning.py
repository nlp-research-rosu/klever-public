#!/usr/bin/env python3
"""Mechanically compare submitted MPY AST with roundedAvgProgram's rule RHS."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess


WORK = Path("/tmp/audit-work/reconstruction")
verification = (WORK / "verification.k").read_text()
marker = "rule roundedAvgProgram =>"
assert verification.count(marker) == 1
tail = verification.split(marker, 1)[1]
lines = tail.splitlines()
term_lines: list[str] = []
started = False
balance = 0
for line in lines:
    stripped = line.strip()
    if not started:
        if stripped.startswith("Module("):
            started = True
        else:
            continue
    term_lines.append(stripped)
    balance += stripped.count("(") - stripped.count(")")
    if started and balance == 0:
        break
assert started and balance == 0
rhs = "\n".join(term_lines)
print("EXTRACTED_RULE_RHS")
print(rhs)
# `.Stmts` is the internal list unit accepted in a K rule.  Concrete MPY
# program syntax denotes the same empty Stmts list by omitting all elements.
rhs_program_syntax = rhs.replace(".Stmts", "")
print("RULE_RHS_IN_CONCRETE_PROGRAM_SYNTAX")
print(rhs_program_syntax)


def parse(command: list[str]):
    print("$ " + " ".join(command))
    completed = subprocess.run(
        command,
        cwd=WORK,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    print(f"EXIT_STATUS={completed.returncode}")
    if completed.returncode != 0:
        print(completed.stdout)
        raise SystemExit(completed.returncode)
    return json.loads(completed.stdout)["term"]


common = [
    "--definition",
    str(WORK / "proof-kompiled"),
    "--sort",
    "Module",
    "--output",
    "json",
]
submitted = parse(["kast", str(WORK / "regenerated-solution.mpy"), *common])
rule_rhs = parse(["kast", "--expression", rhs_program_syntax, *common])
submitted_bytes = json.dumps(submitted, sort_keys=True, separators=(",", ":")).encode()
rhs_bytes = json.dumps(rule_rhs, sort_keys=True, separators=(",", ":")).encode()
print(f"SUBMITTED_KAST_SHA256={hashlib.sha256(submitted_bytes).hexdigest()}")
print(f"RULE_RHS_KAST_SHA256={hashlib.sha256(rhs_bytes).hexdigest()}")
print(f"CONSTRUCTOR_LEVEL_EQUAL={submitted == rule_rhs}")
raise SystemExit(0 if submitted == rule_rhs else 1)
