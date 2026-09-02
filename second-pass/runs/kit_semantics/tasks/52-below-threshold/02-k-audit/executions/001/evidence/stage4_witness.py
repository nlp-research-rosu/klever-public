#!/usr/bin/env python3
"""Concrete satisfying witnesses for all four entry-claim partitions."""

from __future__ import annotations

import importlib.util
from decimal import Decimal


def load_function(path: str, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.below_threshold


candidate = load_function("/candidate/solution.py", "stage4_candidate")
canonical = load_function("/reference/canonical.py", "stage4_canonical")

witnesses = [
    ("empty", [], 0),
    ("int-head", [1, 3], 3),
    ("bool-head", [False, True], 1),
    ("float-head", [0.5, -2], 1),
]

for partition, values, threshold in witnesses:
    claimed = all(value < threshold for value in values)
    got_candidate = candidate(list(values), threshold)
    got_canonical = canonical(list(values), threshold)
    print(
        f"{partition}: values={values!r} threshold={threshold} "
        f"claimed={claimed!r} candidate={got_candidate!r} "
        f"canonical={got_canonical!r}"
    )
    if not (claimed == got_candidate == got_canonical):
        raise SystemExit(1)

for values, threshold in [
    ([Decimal("1.5")], 2),
    ([Decimal("2.0")], 2),
]:
    claimed = all(value < threshold for value in values)
    got_candidate = candidate(list(values), threshold)
    got_canonical = canonical(list(values), threshold)
    print(
        f"supplied-model-gap Decimal: values={values!r} threshold={threshold} "
        f"claimed={claimed!r} candidate={got_candidate!r} "
        f"canonical={got_canonical!r}"
    )
    if not (claimed == got_candidate == got_canonical):
        raise SystemExit(1)
