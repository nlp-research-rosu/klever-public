#!/usr/bin/env python3
"""Minimal false-behavior witnesses for the generated strip semantics."""

from __future__ import annotations

import importlib.util
import json
import re
import subprocess
from pathlib import Path


WORK = Path("/tmp/audit-work/reconstruction")
DEFINITION = WORK / "semantic-haskell-fresh-kompiled"


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_bored


def run_k(text: str) -> tuple[int, list[str]]:
    command = [
        "krun",
        "solution.mpy",
        "--definition",
        str(DEFINITION),
        f"-cINPUT={json.dumps(text)}",
        "--output",
        "pretty",
    ]
    completed = subprocess.run(
        command,
        cwd=WORK,
        text=True,
        capture_output=True,
        check=False,
    )
    match = re.search(r"<result>\s*([0-9-]+)\s*</result>", completed.stdout)
    if completed.returncode != 0 or match is None:
        raise RuntimeError(
            f"krun failed code={completed.returncode} "
            f"stdout={completed.stdout!r} stderr={completed.stderr!r}"
        )
    return int(match.group(1)), command


canonical = load_entry("unicode_canonical", Path("/reference/canonical.py"))
submitted = load_entry("unicode_submitted", WORK / "solution.py")

cases = [
    ("ASCII control", "No.\tI agree"),
    ("U+0085 NEXT LINE", "No.\u0085I agree"),
    ("U+00A0 NO-BREAK SPACE", "No.\u00a0I agree"),
    ("U+1680 OGHAM SPACE MARK", "No.\u1680I agree"),
    ("U+2003 EM SPACE", "No.\u2003I agree"),
    ("U+3000 IDEOGRAPHIC SPACE", "No.\u3000I agree"),
    ("trailing U+00A0 after I-space", "I \u00a0"),
]

semantic_mismatches = 0
for label, text in cases:
    got_k, command = run_k(text)
    got_submitted = submitted(text)
    got_canonical = canonical(text)
    print(f"COMMAND: {' '.join(command)}")
    print(
        f"case={label!r} input={text!r} K={got_k} "
        f"submitted_python={got_submitted} canonical_python={got_canonical}"
    )
    semantic_mismatches += got_k != got_submitted

print(f"case_count={len(cases)}")
print(f"K_vs_submitted_mismatch_count={semantic_mismatches}")
# The nonzero status intentionally records that the semantic model diverges.
raise SystemExit(1 if semantic_mismatches else 0)
