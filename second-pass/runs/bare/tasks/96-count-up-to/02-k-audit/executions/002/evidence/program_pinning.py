#!/usr/bin/env python3
"""Mechanically compare parsed program terms in solution.mpy, semantic.k, spec.k."""

from __future__ import annotations

import hashlib
import shlex
import subprocess
from pathlib import Path


root = Path("/tmp/audit-work/96-count-up-to")
candidate = root / "candidate"
build = root / "build"
definition = build / "semantic-kompiled"


def extract_balanced_module(text: str, start: int = 0) -> str:
    begin = text.index("Module(", start)
    depth = 0
    in_string = False
    escaped = False
    for index in range(begin, len(text)):
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
                return text[begin : index + 1]
    raise AssertionError("unbalanced Module term")


solution_term = (candidate / "solution.mpy").read_text(encoding="utf-8").strip()
semantic_text = (candidate / "semantic.k").read_text(encoding="utf-8")
spec_text = (candidate / "spec.k").read_text(encoding="utf-8")
semantic_term = extract_balanced_module(semantic_text, semantic_text.index("rule <k>"))
spec_term = extract_balanced_module(
    spec_text, spec_text.index("claim [count-up-to-correct]")
)


def program_surface(term: str) -> str:
    """Erase only generated-list unit names unavailable to the program scanner."""
    print(
        "INERT_LIST_UNIT_NORMALIZATION",
        f"Exprs={term.count('.Exprs')}",
        f"Stmts={term.count('.Stmts')}",
    )
    return (
        term.replace(", .Exprs", "")
        .replace(".Exprs", "")
        .replace(".Stmts", "")
    )


term_paths = {
    "solution": candidate / "solution.mpy",
    "semantic-lowering-lhs": build / "semantic-lowering-program.mpy",
    "entry-claim-lhs": build / "entry-claim-program.mpy",
}
term_paths["semantic-lowering-lhs"].write_text(
    program_surface(semantic_term) + "\n", encoding="utf-8"
)
term_paths["entry-claim-lhs"].write_text(
    program_surface(spec_term) + "\n", encoding="utf-8"
)

parsed = {}
for label, path in term_paths.items():
    command = [
        "kast",
        str(path),
        "--definition",
        str(definition),
        "--module",
        "MPY-SYNTAX",
        "--sort",
        "Program",
        "--output",
        "kast",
    ]
    print("COMMAND:", shlex.join(command))
    completed = subprocess.run(command, capture_output=True, text=True)
    print("EXIT_STATUS:", completed.returncode)
    if completed.stderr:
        print("STDERR:", completed.stderr.rstrip())
    assert completed.returncode == 0, completed.stdout + completed.stderr
    parsed[label] = completed.stdout
    print(
        f"PARSED_SHA256 {label} "
        f"{hashlib.sha256(completed.stdout.encode()).hexdigest()}"
    )

assert parsed["solution"] == parsed["semantic-lowering-lhs"]
assert parsed["solution"] == parsed["entry-claim-lhs"]
print("CONSTRUCTOR_LEVEL_IDENTITY_OK solution semantic-lowering-lhs entry-claim-lhs")
