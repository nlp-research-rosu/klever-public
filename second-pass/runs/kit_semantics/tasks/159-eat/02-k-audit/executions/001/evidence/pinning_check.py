#!/usr/bin/env python3
"""Constructor-level comparison of solution.mpy with both claimed closure bodies."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/159-eat")
SPEC = SCRATCH / "spec.k"
DEFINITION = SCRATCH / "fresh-verification-kompiled"


def matching_paren(text: str, opening: int) -> int:
    depth = 0
    quoted = False
    escaped = False
    for index in range(opening, len(text)):
        char = text[index]
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
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return index
    raise ValueError("unbalanced parentheses")


def top_level_arguments(text: str) -> list[str]:
    result: list[str] = []
    start = 0
    depth = 0
    quoted = False
    escaped = False
    for index, char in enumerate(text):
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
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
        elif char == "," and depth == 0:
            result.append(text[start:index].strip())
            start = index + 1
    result.append(text[start:].strip())
    return result


def parse_program(path: Path) -> dict:
    completed = subprocess.run(
        [
            "kast",
            str(path),
            "--definition",
            str(DEFINITION),
            "--output",
            "json",
        ],
        check=True,
        text=True,
        capture_output=True,
    )
    return json.loads(completed.stdout)


spec_text = SPEC.read_text()
marker = "closureVal("
offset = 0
closure_bodies: list[str] = []
while True:
    occurrence = spec_text.find(marker, offset)
    if occurrence < 0:
        break
    opening = occurrence + len("closureVal")
    closing = matching_paren(spec_text, opening)
    arguments = top_level_arguments(spec_text[opening + 1 : closing])
    if len(arguments) != 6:
        raise AssertionError(
            f"closure at {occurrence} has {len(arguments)} top-level arguments"
        )
    if arguments[:4] != ['"number"', '"need"', '"remaining"', ".ParamNames"]:
        raise AssertionError(f"unexpected closure parameters: {arguments[:4]}")
    if arguments[5] != "0":
        raise AssertionError(f"unexpected defining environment: {arguments[5]}")
    closure_bodies.append(arguments[4])
    offset = closing + 1

print(f"closure_occurrences={len(closure_bodies)}")
if len(closure_bodies) != 2:
    raise AssertionError("expected one closure body in each of two entry claims")

solution_kast = parse_program(SCRATCH / "solution.mpy")
solution_digest = hashlib.sha256(
    json.dumps(solution_kast, sort_keys=True, separators=(",", ":")).encode()
).hexdigest()
print(f"solution_kast_sha256={solution_digest}")

all_equal = True
for index, body in enumerate(closure_bodies, 1):
    # Claims may spell the internal empty Stmts unit explicitly. The MPY
    # surface program grammar spells the same list identity by omission.
    surface_body = body.replace(".Stmts", "")
    wrapper = (
        'Module(FuncDef("eat", Params("number", "need", "remaining"),\n'
        + surface_body
        + "))\n"
    )
    wrapper_path = SCRATCH / f"claim-{index}-program.mpy"
    wrapper_path.write_text(wrapper)
    claim_kast = parse_program(wrapper_path)
    claim_digest = hashlib.sha256(
        json.dumps(claim_kast, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    equal = claim_kast == solution_kast
    all_equal = all_equal and equal
    print(f"claim_{index}_kast_sha256={claim_digest}")
    print(f"claim_{index}_constructor_equal={equal}")

print(f"all_claim_bodies_constructor_equal={all_equal}")
if not all_equal:
    raise SystemExit(1)
