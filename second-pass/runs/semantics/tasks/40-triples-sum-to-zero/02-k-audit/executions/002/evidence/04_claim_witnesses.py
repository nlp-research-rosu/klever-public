#!/usr/bin/env python3
"""Ground witnesses for every fixed-length entry precondition."""

from __future__ import annotations

import importlib.util
import itertools


def load(path: str, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.triples_sum_to_zero


canonical = load(
    "/tmp/audit-work/reconstruction/canonical.py", "trusted_canonical_witness"
)
candidate = load("/tmp/audit-work/reconstruction/solution.py", "candidate_witness")


def has_zero_triple(values: list[int]) -> bool:
    return any(sum(triple) == 0 for triple in itertools.combinations(values, 3))


for length in range(7):
    values = [0] * length
    claimed = has_zero_triple(values)
    trusted = canonical(list(values))
    submitted = candidate(list(values))
    print(
        f"claim_length={length} witness={values} "
        f"claimed_summary={claimed} canonical={trusted} candidate={submitted}"
    )
    assert claimed == trusted == submitted
print("ALL_ENTRY_PRECONDITIONS_SATISFIABLE=true")
