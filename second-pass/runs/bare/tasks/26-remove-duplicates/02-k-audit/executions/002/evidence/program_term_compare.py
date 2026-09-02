#!/usr/bin/env python3
"""Mechanically compare the entry claim's Pgm term with solution.mpy."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


REBUILD = Path("/tmp/audit-work/rebuild")
spec_text = (REBUILD / "spec.k").read_text()
marker = "// End-to-end theorem"
claim_region = spec_text.index(marker)
k_start = spec_text.index("<k>", claim_region) + len("<k>")
k_end = spec_text.index("=> .K", k_start)
claim_program = spec_text[k_start:k_end].strip()
# `.Strings` is the internal unit constructor for the empty `List{String, ","}`.
# The submitted concrete program spells the same constructor with empty surface
# list syntax. Normalize that one proven syntax-only difference before parsing.
normalized_claim_program = claim_program.replace(
    "FreeVars(.Strings)", "FreeVars()"
)


def parse(arguments: list[str]) -> dict[str, object]:
    result = subprocess.run(
        arguments,
        cwd=REBUILD,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    print("COMMAND: " + " ".join(arguments))
    print(f"EXIT_STATUS: {result.returncode}")
    if result.returncode != 0:
        print(result.stdout)
        raise SystemExit(result.returncode)
    return json.loads(result.stdout)


common = [
    "kast",
    "--definition",
    "semantic-kompiled",
    "--module",
    "MPY-SYNTAX",
    "--sort",
    "Pgm",
    "--output",
    "json",
]
submitted_ast = parse(common + ["solution.mpy"])
claim_ast = parse(common + ["--expression", normalized_claim_program])
submitted_json = json.dumps(submitted_ast, sort_keys=True, separators=(",", ":"))
claim_json = json.dumps(claim_ast, sort_keys=True, separators=(",", ":"))

print(f"extracted_claim_chars={len(claim_program)}")
print(
    "syntax_normalization="
    "FreeVars(.Strings) -> FreeVars() (empty List{String, \",\"} unit)"
)
print(
    "submitted_ast_sha256="
    + hashlib.sha256(submitted_json.encode()).hexdigest()
)
print("claim_ast_sha256=" + hashlib.sha256(claim_json.encode()).hexdigest())
print(f"constructor_ast_identical={submitted_ast == claim_ast}")
if submitted_ast != claim_ast:
    raise SystemExit(1)
