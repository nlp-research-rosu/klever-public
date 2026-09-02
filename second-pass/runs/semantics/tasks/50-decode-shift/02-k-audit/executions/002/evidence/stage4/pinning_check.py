#!/usr/bin/env python3
"""Mechanically compare the proof closure macro with the translated function body."""

from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path


WORK = Path("/tmp/audit-work/fresh")
EVIDENCE = Path("/audit-output/evidence/stage4")


def balanced_close(text: str, opening: int) -> int:
    depth = 0
    quote = False
    escaped = False
    for index in range(opening, len(text)):
        char = text[index]
        if quote:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quote = False
            continue
        if char == '"':
            quote = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return index
    raise ValueError("unbalanced constructor")


def split_top_level(text: str) -> list[str]:
    pieces = []
    start = 0
    depth = 0
    quote = False
    escaped = False
    for index, char in enumerate(text):
        if quote:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quote = False
            continue
        if char == '"':
            quote = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
        elif char == "," and depth == 0 and len(pieces) < 2:
            pieces.append(text[start:index].strip())
            start = index + 1
    pieces.append(text[start:].strip())
    return pieces


translated = (WORK / "solution.regenerated.mpy").read_text(encoding="utf-8")
marker = 'FuncDef("decode_shift"'
start = translated.index(marker)
opening = translated.index("(", start)
closing = balanced_close(translated, opening)
arguments = split_top_level(translated[opening + 1 : closing])
assert len(arguments) == 3
assert arguments[0] == '"decode_shift"'
assert "".join(arguments[1].split()) == 'Params("s")'
body = arguments[2]

# The external program parser uses the one-element List surface form `"s"`;
# its KORE expansion is the same ParamNames constructor list used by the rule parser.
expected = f'closureVal("s", {body}, 0)'
(EVIDENCE / "expected-closure-from-solution.term").write_text(
    expected + "\n", encoding="utf-8"
)

common = [
    "kast",
    "--definition",
    str(WORK / "verification-kompiled"),
    "--module",
    "VERIFICATION-WITH-LOOP",
    "--sort",
    "Val",
    "--expand-macros",
    "--output",
    "kore",
]
macro_run = subprocess.run(
    [*common, "--expression", "decodeClosure"],
    check=True,
    capture_output=True,
    text=True,
)
expected_run = subprocess.run(
    [*common, "--expression", expected],
    check=True,
    capture_output=True,
    text=True,
)
(EVIDENCE / "macro-expanded.kore").write_text(macro_run.stdout, encoding="utf-8")
(EVIDENCE / "expected-from-solution.kore").write_text(
    expected_run.stdout, encoding="utf-8"
)
assert macro_run.stdout == expected_run.stdout

digest = hashlib.sha256(macro_run.stdout.encode("utf-8")).hexdigest()
print("translated_function=decode_shift")
print("parameter_constructor_identity=true")
print("body_constructor_identity=true")
print("expanded_closure_kore_identity=true")
print(f"expanded_kore_sha256={digest}")
print(f"expanded_kore_bytes={len(macro_run.stdout.encode('utf-8'))}")
