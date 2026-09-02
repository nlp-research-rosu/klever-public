#!/usr/bin/env python3
"""Mechanical checks connecting regenerated MPython to the target claim."""

from __future__ import annotations

import re
from pathlib import Path


def balanced_ctor(source: str, ctor: str, occurrence: int = 0) -> str:
    matches = list(re.finditer(rf"\b{re.escape(ctor)}\s*\(", source))
    if occurrence >= len(matches):
        raise AssertionError(f"missing occurrence {occurrence} of {ctor}")
    start = matches[occurrence].start()
    open_index = source.find("(", start)
    depth = 0
    in_string = False
    escaped = False
    for index in range(open_index, len(source)):
        char = source[index]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
        elif char == '"':
            in_string = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return source[start : index + 1]
    raise AssertionError(f"unbalanced {ctor}")


def normalize(term: str) -> str:
    return re.sub(r"\s+", "", term)


regenerated = Path(
    "/tmp/audit-work/48-is-palindrome-audit/solution.regenerated.mpy"
).read_text(encoding="utf-8")
submitted = Path("/candidate/solution.mpy").read_text(encoding="utf-8")
spec = Path("/candidate/spec.k").read_text(encoding="utf-8")

if regenerated.encode() != Path("/candidate/solution.mpy").read_bytes():
    raise AssertionError("regenerated solution.mpy is not byte-identical")

program_func = balanced_ctor(regenerated, "FuncDef")
claim_func = balanced_ctor(spec, "FuncDef", 0)
closure_body = balanced_ctor(spec, "Return", 1)
program_body = balanced_ctor(regenerated, "Return", 0)

if normalize(program_func) != normalize(claim_func):
    raise AssertionError("claim FuncDef differs from regenerated program FuncDef")
if normalize(program_body) != normalize(closure_body):
    raise AssertionError("destination closure body differs from regenerated body")

print("COMMAND: python3 /audit-output/evidence/pinning_check.py")
print("REGENERATION_BYTE_IDENTITY=PASS")
print("CLAIM_FUNCDEF_CONSTRUCTOR_IDENTITY=PASS")
print("DESTINATION_CLOSURE_BODY_IDENTITY=PASS")
print("OBSERVATION_SUFFIX=Assign(Name(\"__result\"), Call(Name(\"is_palindrome\"), str(S)))")
print("PINNING_RESULT=PASS")
