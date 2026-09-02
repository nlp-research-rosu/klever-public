#!/usr/bin/env python3
"""Mechanically compare the claim-executed module with trusted solution.mpy."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path


def extract_rule_rhs(source: str, marker: str) -> str:
    start = source.index(marker) + len(marker)
    tail = source[start:].lstrip()
    term_start = tail.index("Module(")
    tail = tail[term_start:]
    depth = 0
    quoted = False
    escaped = False
    started = False
    for index, char in enumerate(tail):
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
            started = True
        elif char == ")":
            depth -= 1
            if started and depth == 0:
                return tail[: index + 1]
    raise ValueError("could not find balanced simplifyProgram RHS")


def parsed_json(term: str, definition: Path) -> bytes:
    process = subprocess.run(
        [
            "kast",
            "--definition",
            str(definition),
            "--module",
            "VERIFICATION",
            "--sort",
            "Module",
            "--expression",
            term,
            "--output",
            "json",
        ],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if process.stderr:
        print(process.stderr.decode(), file=sys.stderr)
    # Parse and canonically re-encode so irrelevant JSON whitespace cannot differ.
    value = json.loads(process.stdout)
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.simplify


def main() -> int:
    root = Path("/tmp/audit-work/reconstruction")
    verification = (root / "verification.k").read_text()
    submitted = (root / "solution.mpy").read_text().strip()
    extracted = extract_rule_rhs(verification, "rule simplifyProgram =>").strip()
    definition = root / "audit-verification-kompiled"

    submitted_json = parsed_json(submitted, definition)
    extracted_json = parsed_json(extracted, definition)
    print(f"submitted_text_sha256={hashlib.sha256(submitted.encode()).hexdigest()}")
    print(f"extracted_text_sha256={hashlib.sha256(extracted.encode()).hexdigest()}")
    print(f"submitted_kast_sha256={hashlib.sha256(submitted_json).hexdigest()}")
    print(f"extracted_kast_sha256={hashlib.sha256(extracted_json).hexdigest()}")
    print(f"constructor_terms_equal={submitted_json == extracted_json}")
    print("extracted_term:")
    print(extracted)

    canonical = load_entry(
        Path("/tmp/audit-work/reference/canonical.py"), "pinning_canonical"
    )
    generated = load_entry(root / "solution.py", "pinning_generated")
    witnesses = [
        (1, 1, 1, 1),
        (1, 2, 1, 1),
        (1, 5, 5, 1),
    ]
    for a, b, c, d in witnesses:
        claimed = ((a * c) % (b * d)) == 0
        x, n = f"{a}/{b}", f"{c}/{d}"
        print(
            json.dumps(
                {
                    "A": a,
                    "B": b,
                    "C": c,
                    "D": d,
                    "precondition": min(a, b, c, d) > 0,
                    "claimed_result": claimed,
                    "canonical_result": canonical(x, n),
                    "generated_result": generated(x, n),
                },
                sort_keys=True,
                separators=(",", ":"),
            )
        )

    return 0 if submitted_json == extracted_json else 1


if __name__ == "__main__":
    raise SystemExit(main())
