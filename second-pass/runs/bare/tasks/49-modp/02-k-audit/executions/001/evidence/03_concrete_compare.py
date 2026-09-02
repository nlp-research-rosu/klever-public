#!/usr/bin/env python3
"""Run the freshly compiled generated semantics and compare with Python."""

from __future__ import annotations

import importlib.util
import json
import re
import subprocess
from pathlib import Path
from typing import Any, Callable


FRESH = Path("/tmp/audit-work/fresh")
DEFINITION = FRESH / "concrete-kompiled"
PROGRAM = FRESH / "solution.mpy"
CANONICAL_PATH = Path("/reference/canonical.py")
GENERATED_PATH = FRESH / "solution.py"
RESULT_RE = re.compile(r"result\s*\(\s*(-?\d+)\s*\)")


def load_entry(path: Path, module_name: str) -> Callable[[int, int], Any]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.modp


def observe(fn: Callable[[int, int], Any], n: int, p: int) -> dict[str, Any]:
    try:
        return {"kind": "return", "value": fn(n, p)}
    except Exception as err:
        return {
            "kind": "exception",
            "type": type(err).__name__,
            "message": str(err),
        }


canonical = load_entry(CANONICAL_PATH, "trusted_canonical_concrete")
generated = load_entry(GENERATED_PATH, "candidate_generated_concrete")
cases = [
    (3, 5),
    (1101, 101),
    (3, 11),
    (100, 101),
    (0, 101),
    (0, 1),
    (1, 1),
    (1, 2),
    (2, 3),
    (10_000, 65_537),
]

records = []
failures = []
for n, p in cases:
    argv = [
        "krun",
        str(PROGRAM),
        "--definition",
        str(DEFINITION),
        f"-cN={n}",
        f"-cP={p}",
    ]
    print("$ " + " ".join(argv))
    completed = subprocess.run(
        argv,
        cwd=FRESH,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    print(completed.stdout, end="" if completed.stdout.endswith("\n") else "\n")
    print(f"[exit {completed.returncode}]")
    matches = RESULT_RE.findall(completed.stdout)
    k_observed: dict[str, Any]
    if completed.returncode == 0 and len(matches) == 1:
        k_observed = {"kind": "return", "value": int(matches[0])}
    else:
        k_observed = {
            "kind": "krun_failure",
            "exit": completed.returncode,
            "result_matches": matches,
        }
    generated_observed = observe(generated, n, p)
    canonical_observed = observe(canonical, n, p)
    record = {
        "input": [n, p],
        "k": k_observed,
        "generated_python": generated_observed,
        "canonical_python": canonical_observed,
        "k_matches_generated": k_observed == generated_observed,
        "k_matches_canonical": k_observed == canonical_observed,
    }
    records.append(record)
    if not record["k_matches_generated"]:
        failures.append(record)

print("CONCRETE_COMPARISON")
print(json.dumps(records, indent=2, sort_keys=True))
print(f"k_vs_generated_mismatch_count={len(failures)}")
print(
    "k_vs_canonical_mismatch_count="
    + str(sum(not r["k_matches_canonical"] for r in records))
)
raise SystemExit(1 if failures else 0)
