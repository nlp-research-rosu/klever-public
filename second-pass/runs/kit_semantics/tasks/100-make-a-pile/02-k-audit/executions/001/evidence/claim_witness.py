#!/usr/bin/env python3
"""Ground witnesses for the entry precondition and claimed finishPile value."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


def load(name: str, path: Path):
    spec = spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


scratch = Path("/tmp/audit-work/reconstruction")
canonical = load("canonical_witness", scratch / "canonical.py")
candidate = load("candidate_witness", scratch / "solution.py")


def finish_pile(acc, n, i):
    while i < n:
        acc = acc + [n + 2 * i]
        i += 1
    return acc


for n in (1, 2, 3, 5):
    assert n > 0
    summary = finish_pile([], n, 0)
    expected = canonical.make_a_pile(n)
    actual = candidate.make_a_pile(n)
    print(
        f"N={n}; precondition_N_gt_0=true; "
        f"finishPile={summary!r}; canonical={expected!r}; candidate={actual!r}"
    )
    assert summary == expected == actual

print("CLAIM_WITNESSES=PASS")
