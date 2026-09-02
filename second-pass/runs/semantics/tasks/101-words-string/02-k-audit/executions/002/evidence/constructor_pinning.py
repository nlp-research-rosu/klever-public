#!/usr/bin/env python3
"""Mechanically compare the submitted MPY module to the theorem's closure.

The K parser expands both terms to constructor-level JSON.  The only admitted
normalization is the semantic representation of a top-level FuncDef as a
closureVal: Params becomes the closure's ParamNames, the exact Stmts subtree is
preserved, and the defining scope is 0.
"""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path


ROOT = Path("/tmp/audit-work/101-words-string-independent-audit")
DEFINITION = ROOT / "verification-kompiled"


def split_top_level(text: str) -> list[str]:
    parts: list[str] = []
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
        elif char == '"':
            quoted = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
        elif char == "," and depth == 0:
            parts.append(text[start:index].strip())
            start = index + 1
    parts.append(text[start:].strip())
    return parts


def matching_paren(text: str, open_index: int) -> int:
    depth = 0
    quoted = False
    escaped = False
    for index in range(open_index, len(text)):
        char = text[index]
        if quoted:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
        elif char == '"':
            quoted = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return index
    raise AssertionError("unbalanced closureVal term")


def kast_json(*args: str) -> dict:
    proc = subprocess.run(
        ["kast", "--definition", str(DEFINITION), "--output", "json", *args],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    return json.loads(proc.stdout)["term"]


submitted = kast_json("--input", "program", str(ROOT / "solution.mpy"))

verification = (ROOT / "verification.k").read_text()
marker = "rule wordsStringFunction =>"
after_rule = verification.index(marker) + len(marker)
closure_start = verification.index("closureVal(", after_rule)
open_paren = verification.index("(", closure_start)
close_paren = matching_paren(verification, open_paren)
closure_args = split_top_level(verification[open_paren + 1 : close_paren])
if len(closure_args) != 3:
    raise AssertionError(f"expected three closureVal arguments: {closure_args!r}")
params, body, defining_scope = closure_args

normalized_params = "".join(params.split())
if normalized_params != '("s",.ParamNames)':
    raise AssertionError(f"unexpected theorem parameters: {params}")
if defining_scope.strip() != "0":
    raise AssertionError(f"unexpected theorem defining scope: {defining_scope}")

surface_body = body.replace(
    '(Str(","), Str(" "), .Exprs)',
    'Str(","), Str(" ")',
)
surface_body, empty_exprs = re.subn(r",\s*\.Exprs\)", ", )", surface_body)
surface_body, empty_stmts = re.subn(r"\s*\.Stmts\s*$", "", surface_body)
if empty_exprs != 1 or empty_stmts != 1:
    raise AssertionError(
        f"unexpected list normalization counts: Exprs={empty_exprs}, Stmts={empty_stmts}"
    )
reconstructed_text = (
    'Module(FuncDef("words_string", Params("s"), ' + surface_body + "))"
)
reconstructed = kast_json(
    "--sort",
    "Module",
    "--expression",
    reconstructed_text,
)

if submitted != reconstructed:
    raise AssertionError("submitted MPY constructors differ from theorem closure")

print("function_name=words_string")
print("parameter_sequence=(s)")
print("defining_scope=0")
print("constructor_trees_equal=true")
