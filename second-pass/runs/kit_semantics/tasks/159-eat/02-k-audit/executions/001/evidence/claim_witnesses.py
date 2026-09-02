#!/usr/bin/env python3
"""Concrete satisfying witnesses for both symbolic entry preconditions."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.eat


canonical = load("canonical_witness", Path("/reference/canonical.py"))
generated = load("generated_witness", Path("/tmp/audit-work/159-eat/solution.py"))

witnesses = [
    ("eat-enough", (5, 6, 10), [11, 4]),
    ("eat-insufficient", (2, 11, 5), [7, 0]),
]

for label, (number, need, remaining), claimed in witnesses:
    in_prompt_domain = all(0 <= value <= 1000 for value in (number, need, remaining))
    branch_guard = (
        need <= remaining if label == "eat-enough" else need > remaining
    )
    canonical_result = canonical(number, need, remaining)
    generated_result = generated(number, need, remaining)
    print(
        f"{label}: args={(number, need, remaining)} "
        f"domain={in_prompt_domain} guard={branch_guard} "
        f"claimed_heap_list={claimed} canonical={canonical_result} "
        f"generated={generated_result}"
    )
    if not (
        in_prompt_domain
        and branch_guard
        and claimed == canonical_result == generated_result
    ):
        raise SystemExit(1)
