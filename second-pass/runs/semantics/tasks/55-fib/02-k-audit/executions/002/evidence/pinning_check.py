#!/usr/bin/env python3
"""Mechanical constructor-level comparison of the claim program and solution.mpy."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path


def strip_layout_outside_strings(text: str) -> str:
    output: list[str] = []
    in_string = False
    escaped = False
    for character in text:
        if in_string:
            output.append(character)
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                in_string = False
        elif character == '"':
            in_string = True
            output.append(character)
        elif not character.isspace():
            output.append(character)
    assert not in_string
    return "".join(output)


solution = Path("/candidate/solution.mpy").read_text(encoding="utf-8")
verification = Path("/candidate/verification.k").read_text(encoding="utf-8")
spec = Path("/candidate/spec.k").read_text(encoding="utf-8")

body_match = re.search(
    r"rule\s+fibBody\s*=>\s*(.*?)\n\s*rule\s+fibClosure\s*=>",
    verification,
    re.DOTALL,
)
program_match = re.search(
    r"rule\s+fibProgram\s*=>\s*(Module\(FuncDef\(\"fib\",\s*Params\(\"n\"\),\s*fibBody\)\))",
    verification,
    re.DOTALL,
)
assert body_match is not None
assert program_match is not None

body = body_match.group(1).strip()
program = program_match.group(1).replace("fibBody", body)
normalized_solution = strip_layout_outside_strings(solution)
normalized_program = strip_layout_outside_strings(program)

assert normalized_program == normalized_solution
assert '#loadAll(fibProgram) ~> Call(Name("fib"), Int(N:Int))' in spec
assert 'requires N >=Int 0' in spec
assert 'imports MPY' in verification
assert "<k>" not in verification, "verification.k unexpectedly contains an operational rewrite"

digest = hashlib.sha256(normalized_program.encode()).hexdigest()
print(f"normalized_constructor_sha256={digest}")
print("trusted_regenerated_solution_mpy_equals_expanded_fibProgram=true")
print("entry_claim_executes_fibProgram_then_calls_bound_name_fib=true")
print("verification_operational_bridge_count=0")
print("pinning_status=PASS")
