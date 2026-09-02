#!/usr/bin/env python3
"""Mechanically compare submitted and claim-embedded MPY constructor terms."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path("/tmp/audit-work/fresh")
DEFINITION = ROOT / "audit-verification-kompiled"


def balanced_inside(text: str, open_index: int) -> tuple[str, int]:
    if text[open_index] != "(":
        raise ValueError("open_index is not an opening parenthesis")
    depth = 1
    in_string = False
    escaped = False
    for index in range(open_index + 1, len(text)):
        char = text[index]
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
                return text[open_index + 1 : index], index
    raise ValueError("unbalanced parentheses")


def top_level_args(text: str) -> list[str]:
    arguments: list[str] = []
    start = 0
    depth = 0
    in_string = False
    escaped = False
    for index, char in enumerate(text):
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
        elif char == "," and depth == 0:
            arguments.append(text[start:index].strip())
            start = index + 1
    arguments.append(text[start:].strip())
    return arguments


def parse_module(path: Path) -> dict[str, object]:
    process = subprocess.run(
        [
            "kast",
            str(path),
            "--definition",
            str(DEFINITION),
            "--module",
            "VERIFICATION",
            "--sort",
            "Module",
            "--output",
            "json",
        ],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if process.stderr:
        print(f"KAST_STDERR[{path.name}]={process.stderr.strip()}")
    return json.loads(process.stdout)


verification = (ROOT / "verification.k").read_text()

load_marker = "=> #loadAll("
load_start = verification.index(load_marker) + len(load_marker) - 1
load_module, _ = balanced_inside(verification, load_start)

closure_marker = "=> closureVal("
closure_start = verification.index(closure_marker) + len(closure_marker) - 1
closure_inside, _ = balanced_inside(verification, closure_start)
closure_args = top_level_args(closure_inside)
if len(closure_args) != 4:
    raise AssertionError(f"expected four closureVal arguments, got {len(closure_args)}")
closure_body = closure_args[2]
closure_module = (
    'Module(FuncDef("get_odd_collatz", Params("n"),\n'
    + closure_body
    + "))\n"
)

# `.Exprs` is K's internal unit for the surface syntax's optional expression
# sequence; the trusted translator prints the same unit as an empty argument.
load_module = load_module.replace("ListExpr(.Exprs)", "ListExpr()")
closure_module = closure_module.replace("ListExpr(.Exprs)", "ListExpr()")

load_path = ROOT / "audit-extracted-load-module.mpy"
closure_path = ROOT / "audit-extracted-closure-module.mpy"
load_path.write_text(load_module + "\n")
closure_path.write_text(closure_module)

submitted_json = parse_module(ROOT / "solution.mpy")
load_json = parse_module(load_path)
closure_json = parse_module(closure_path)


def json_digest(value: dict[str, object]) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


print(f"SUBMITTED_PARSED_SHA256={json_digest(submitted_json)}")
print(f"LOAD_MODULE_PARSED_SHA256={json_digest(load_json)}")
print(f"CLOSURE_MODULE_PARSED_SHA256={json_digest(closure_json)}")
print(f"LOAD_MODULE_EQUALS_SUBMITTED={load_json == submitted_json}")
print(f"CLOSURE_BODY_EQUALS_SUBMITTED={closure_json == submitted_json}")
print(f"CLOSURE_ARGUMENT_1={closure_args[0]}")
print(f"CLOSURE_ARGUMENT_2={closure_args[1]}")
print(f"CLOSURE_ARGUMENT_4={closure_args[3]}")
print("NORMALIZATION=ListExpr(.Exprs) -> ListExpr() (empty Exprs surface form)")

assert load_json == submitted_json
assert closure_json == submitted_json
