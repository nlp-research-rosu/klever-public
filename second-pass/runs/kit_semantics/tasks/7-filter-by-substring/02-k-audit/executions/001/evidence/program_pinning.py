#!/usr/bin/env python3
"""Compare the submitted MPY term with the entry claim's embedded Module term."""

from __future__ import annotations

import hashlib
import re
import subprocess
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/reconstruction")
DEFINITION = SCRATCH / "reviewer-verification-kompiled"


def extract_balanced_module(spec: str) -> str:
    load_at = spec.index("#loadAll(")
    start = spec.index("Module(", load_at)
    depth = 0
    in_string = False
    escaped = False
    for index in range(start, len(spec)):
        char = spec[index]
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
                return spec[start : index + 1] + "\n"
    raise ValueError("unterminated embedded Module term")


def kast(term: str) -> bytes:
    process = subprocess.run(
        [
            "kast",
            "/dev/stdin",
            "--definition",
            str(DEFINITION),
            "--module",
            "VERIFICATION",
            "--sort",
            "Module",
            "--output",
            "kore",
        ],
        input=term.encode(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if process.returncode != 0:
        raise RuntimeError(
            f"kast exited {process.returncode}: {process.stderr.decode(errors='replace')}"
        )
    return process.stdout


def to_surface_program(term: str) -> str:
    """Erase explicit internal list units that claim syntax may print."""
    term = re.sub(r",\s*\.ParamNames", "", term)
    term = term.replace(".Exprs", "")
    term = term.replace(".Stmts", "")
    return term


def main() -> int:
    submitted = (SCRATCH / "solution.mpy").read_text()
    embedded_internal = extract_balanced_module((SCRATCH / "spec.k").read_text())
    embedded = to_surface_program(embedded_internal)
    submitted_kore = kast(submitted)
    embedded_kore = kast(embedded)
    print(f"submitted_text_sha256={hashlib.sha256(submitted.encode()).hexdigest()}")
    print(
        "embedded_internal_text_sha256="
        f"{hashlib.sha256(embedded_internal.encode()).hexdigest()}"
    )
    print(f"embedded_surface_text_sha256={hashlib.sha256(embedded.encode()).hexdigest()}")
    print(f"submitted_kore_sha256={hashlib.sha256(submitted_kore).hexdigest()}")
    print(f"embedded_kore_sha256={hashlib.sha256(embedded_kore).hexdigest()}")
    print(f"parsed_terms_equal={submitted_kore == embedded_kore}")
    print(f"embedded_module_bytes={len(embedded.encode())}")
    return 0 if submitted_kore == embedded_kore else 1


if __name__ == "__main__":
    raise SystemExit(main())
