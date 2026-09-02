#!/usr/bin/env python3
"""Mechanically compare the submitted FuncDef with SPEC's closure constructor."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/112-reverse-delete")
EXTRACTED = Path("/audit-output/evidence/claimed_entry_function.mpy")


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
            continue
        if char == '"':
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


def parse_with_kast(path: Path) -> dict:
    completed = subprocess.run(
        [
            "kast",
            str(path),
            "--definition",
            str(SCRATCH / "runtime-kompiled"),
            "--sort",
            "Module",
            "--output",
            "json",
        ],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    )
    return json.loads(completed.stdout)["term"]


def find_funcdef(term: dict) -> dict:
    if term.get("node") == "KApply" and term.get("label", {}).get("name", "").startswith(
        "FuncDef(_,_,_)"
    ):
        return term
    for arg in term.get("args", []):
        found = find_funcdef(arg)
        if found:
            return found
    return {}


def digest(term: dict) -> str:
    encoded = json.dumps(term, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def main() -> int:
    spec = (SCRATCH / "spec.k").read_text(encoding="utf-8")
    spec_start = spec.index("module SPEC")
    closure_start = spec.index("closureVal(", spec_start)
    opening = spec.index("(", closure_start)
    closing = matching_paren(spec, opening)
    params, body, definition_location = split_top_level(spec[opening + 1 : closing])

    # The MPY surface parser renders associative-list units by omission, whereas
    # spec.k may spell the generated K unit tokens explicitly.
    surface_body = body.replace(".Stmts", "").replace(".Exprs", "")
    extracted_text = (
        "Module(\n"
        '  FuncDef("reverse_delete", Params'
        + params
        + ",\n"
        + surface_body
        + "))\n"
    )
    EXTRACTED.write_text(extracted_text, encoding="utf-8")

    submitted = find_funcdef(parse_with_kast(SCRATCH / "solution.mpy"))
    claimed = find_funcdef(parse_with_kast(EXTRACTED))
    if not submitted or not claimed:
        print("ERROR: FuncDef not found")
        return 2

    labels_equal = submitted["label"] == claimed["label"]
    name_equal = submitted["args"][0] == claimed["args"][0]
    params_equal = submitted["args"][1] == claimed["args"][1]
    body_equal = submitted["args"][2] == claimed["args"][2]

    print(f"spec_closure_definition_location={definition_location}")
    print(f"funcdef_constructor_equal={labels_equal}")
    print(f"function_name_equal={name_equal}")
    print(f"parameter_constructor_equal={params_equal}")
    print(f"body_constructor_equal={body_equal}")
    print(f"submitted_body_kast_sha256={digest(submitted['args'][2])}")
    print(f"claimed_body_kast_sha256={digest(claimed['args'][2])}")
    return 0 if all((labels_equal, name_equal, params_equal, body_equal)) else 1


if __name__ == "__main__":
    sys.exit(main())
