#!/usr/bin/env python3
"""Compare the proof's executed closure body with trusted-translated solution.mpy."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


def matching_paren(text: str, start: int) -> int:
    if text[start] != "(":
        raise ValueError("expected opening parenthesis")
    depth = 0
    in_string = False
    escaped = False
    for index in range(start, len(text)):
        character = text[index]
        if in_string:
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                in_string = False
            continue
        if character == '"':
            in_string = True
        elif character == "(":
            depth += 1
        elif character == ")":
            depth -= 1
            if depth == 0:
                return index
    raise ValueError("unbalanced parenthesis")


if len(sys.argv) != 5:
    raise SystemExit(
        "usage: constructor_compare.py SPEC.k SOLUTION.mpy DEFINITION SCRATCH"
    )

spec_path = Path(sys.argv[1])
solution_path = Path(sys.argv[2])
definition = Path(sys.argv[3])
scratch = Path(sys.argv[4])

spec_text = spec_path.read_text()
binding_marker = '"hex_key" |-> closureVal('
binding_start = spec_text.index(binding_marker)
parameter_marker = '("num", .ParamNames),'
parameter_end = spec_text.index(parameter_marker, binding_start) + len(
    parameter_marker
)
body_start = parameter_end
while spec_text[body_start].isspace():
    body_start += 1
if spec_text[body_start] != "(":
    raise AssertionError("closure body is not an explicit Stmts sequence")
body_end = matching_paren(spec_text, body_start)
body = spec_text[body_start + 1 : body_end]
closure_tail = spec_text[body_end + 1 :]
if not closure_tail.lstrip().startswith(",\n                0)"):
    raise AssertionError("unexpected closure parent environment")

synthetic_path = scratch / "claim-closure-as-module.mpy"
synthetic_path.write_text(
    'Module(\n  FuncDef("hex_key", Params("num"),\n'
    + body
    + "))\n"
)


def parse(path: Path) -> dict:
    command = [
        "kast",
        "--definition",
        str(definition),
        "--module",
        "MPY-SYNTAX",
        "--sort",
        "Module",
        "--input",
        "program",
        "--output",
        "json",
        str(path),
    ]
    print("INNER_COMMAND:", " ".join(command))
    completed = subprocess.run(
        command, check=True, stdout=subprocess.PIPE, text=True
    )
    return json.loads(completed.stdout)


solution_kast = parse(solution_path)
claim_kast = parse(synthetic_path)
solution_term = solution_kast["term"]
claim_term = claim_kast["term"]
solution_serialized = json.dumps(
    solution_term, sort_keys=True, separators=(",", ":")
).encode()
claim_serialized = json.dumps(
    claim_term, sort_keys=True, separators=(",", ":")
).encode()
solution_hash = hashlib.sha256(solution_serialized).hexdigest()
claim_hash = hashlib.sha256(claim_serialized).hexdigest()

print(f"SOLUTION_CONSTRUCTOR_SHA256={solution_hash}")
print(f"CLAIM_CONSTRUCTOR_SHA256={claim_hash}")
print(f"FUNCTION_BINDING=hex_key PARAMETER=num PARENT_ENV=0")
print(f"CONSTRUCTOR_TERMS_IDENTICAL={solution_term == claim_term}")

if solution_term != claim_term:
    raise SystemExit(1)
