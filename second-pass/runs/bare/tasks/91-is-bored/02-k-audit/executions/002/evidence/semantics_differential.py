#!/usr/bin/env python3
"""Compare fresh K execution with both Python implementations on boundaries."""

from __future__ import annotations

import importlib.util
import json
import re
import subprocess
from pathlib import Path


WORK = Path("/tmp/audit-work/reconstruction")


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_bored


canonical = load_function(
    "trusted_canonical_kdiff", Path("/tmp/audit-work/trusted/canonical.py")
)
candidate = load_function(
    "submitted_solution_kdiff", WORK / "solution.py"
)

cases = [
    "Hello world",
    "The sky is blue. The sun is shining. I love this weather",
    "",
    ".",
    "I ",
    "I x",
    "I",
    " I x",
    "It x",
    "X.I y",
    "X. I y",
    "I x!",
    "... ! ?  . I count!",
    " I am here?You are there!  I agree",
    "\tI tabbed.\nI newline?\rNot me!",
    "é.I oui",
]

k_mismatches = 0
canonical_mismatches = 0
for text in cases:
    input_term = "-cINPUT=" + json.dumps(text, ensure_ascii=False)
    run = subprocess.run(
        [
            "krun",
            "solution.mpy",
            "--definition",
            "concrete-kompiled",
            input_term,
        ],
        cwd=WORK,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    match = re.search(r"<result>\s*(-?\d+)\s*</result>", run.stdout)
    if run.returncode != 0 or match is None:
        print(
            f"KRUN_ERROR input={text!r} exit={run.returncode} "
            f"output={run.stdout!r}"
        )
        raise SystemExit(2)
    k_value = int(match.group(1))
    candidate_value = candidate(text)
    canonical_value = canonical(text)
    k_ok = k_value == candidate_value
    canonical_ok = k_value == canonical_value
    k_mismatches += not k_ok
    canonical_mismatches += not canonical_ok
    print(
        f"input={text!r} k={k_value} candidate={candidate_value} "
        f"k_matches_candidate={k_ok} canonical={canonical_value} "
        f"k_matches_canonical={canonical_ok}"
    )

print(f"k_vs_candidate_mismatches={k_mismatches}")
print(f"k_vs_canonical_mismatches={canonical_mismatches}")
raise SystemExit(1 if k_mismatches else 0)
