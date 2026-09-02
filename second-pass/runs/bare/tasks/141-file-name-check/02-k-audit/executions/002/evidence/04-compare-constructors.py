#!/usr/bin/env python3
"""Mechanically compare solution.mpy with the pinning claim's Program RHS."""

from __future__ import annotations

import hashlib
import json
import shlex
import subprocess
from pathlib import Path


ROOT = Path("/tmp/audit-work/141-file-name-check")
DEFINITION = ROOT / "audit-verification-kompiled"
source_text = (ROOT / "solution.mpy").read_text()
claim_text = (ROOT / "pinning-spec.k").read_text()

start = claim_text.index("=> Module(") + len("=> ")
end = claim_text.index("\n        </k>", start)
# `.Stmts` is K's explicit unit for the same generated list syntax that the
# concrete `.mpy` printer renders as a blank field.
claim_program_text = claim_text[start:end].replace(".Stmts", "") + "\n"


def parse(expression: str | None, source_path: Path | None) -> dict:
    cmd = [
        "kast",
        "--definition",
        str(DEFINITION),
        "--module",
        "MPY-SYNTAX",
        "--sort",
        "Program",
        "--output",
        "json",
    ]
    if expression is not None:
        cmd.extend(["--expression", expression])
    else:
        assert source_path is not None
        cmd.append(str(source_path))
    printable = cmd.copy()
    if expression is not None:
        printable[-1] = "<pinning-spec.k extracted Program RHS>"
    print("$", shlex.join(printable))
    result = subprocess.run(
        cmd,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    print(result.stderr, end="")
    print("[exit", result.returncode, "]")
    if result.returncode:
        raise SystemExit(result.returncode)
    return json.loads(result.stdout)


source_ast = parse(None, ROOT / "solution.mpy")
claim_ast = parse(claim_program_text, None)
source_canonical = json.dumps(source_ast, sort_keys=True, separators=(",", ":"))
claim_canonical = json.dumps(claim_ast, sort_keys=True, separators=(",", ":"))
print("solution_constructor_sha256:",
      hashlib.sha256(source_canonical.encode()).hexdigest())
print("pinning_rhs_constructor_sha256:",
      hashlib.sha256(claim_canonical.encode()).hexdigest())
print("constructor_terms_equal:", source_ast == claim_ast)
raise SystemExit(0 if source_ast == claim_ast else 1)
