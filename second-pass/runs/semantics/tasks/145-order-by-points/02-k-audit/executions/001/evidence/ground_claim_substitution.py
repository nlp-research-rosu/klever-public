#!/usr/bin/env python3
"""Ground substitutions for the generic entry claim."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load("canonical", Path("/reference/canonical.py"))
candidate = load(
    "candidate",
    Path("/tmp/audit-work/145-order-by-points/solution.py"),
)

for values in ([], [11, 1], [1, 11, -1, -11, -12]):
    canonical_result = canonical.order_by_points(list(values))
    candidate_result = candidate.order_by_points(list(values))
    k_items = ", ".join(map(str, values))
    print(f"input={values}")
    print(
        "specialized_formal_heap_value="
        f"list(sortKeyVS(vCons-sequence({k_items}), digitSumClosure))"
    )
    print(f"canonical_python={canonical_result}")
    print(f"candidate_python={candidate_result}")
    print(f"python_agree={canonical_result == candidate_result}")
    print("formal_term_reducible_in_proof_definition=false")

