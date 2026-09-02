#!/usr/bin/env python3
"""Concrete satisfiable witnesses for all submitted claims."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


candidate = load(
    Path("/tmp/audit-work/94-skjkasdkd/source/solution.py"),
    "ground_candidate_94",
)
canonical = load(Path("/reference/canonical.py"), "ground_canonical_94")

checks = [
    ("is_prime_from pre N>=2,D>=2", candidate.is_prime_from(2, 2), True),
    ("is_prime unrestricted N", candidate.is_prime(1), False),
    ("choose_prime unrestricted N,BEST", candidate.choose_prime(5, 3), 5),
    ("largest_prime integer list", candidate.largest_prime([4, 11, 3]), 11),
    ("digit_sum unrestricted N", candidate.digit_sum(123), 6),
    ("candidate entry integer list", candidate.skjkasdkd([4, 11, 3]), 2),
    ("canonical entry same list", canonical.skjkasdkd([4, 11, 3]), 2),
]

failures = 0
for label, actual, expected in checks:
    ok = actual == expected
    print(f"{label}: actual={actual!r} expected={expected!r} pass={ok}")
    failures += not ok
print(f"SUMMARY checks={len(checks)} failures={failures}")
raise SystemExit(1 if failures else 0)
