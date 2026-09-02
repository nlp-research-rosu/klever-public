#!/usr/bin/env python3
"""Ground witnesses for the entry claim's IntSeq summary."""

import importlib.util
from pathlib import Path


def load(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, Path(path))
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sum_product


canonical = load(
    "/tmp/audit-work/8-sum-product-audit-002/trusted/canonical.py", "canonical"
)
candidate = load(
    "/tmp/audit-work/8-sum-product-audit-002/work/solution.py", "candidate"
)

for values in ([], [2], [2, -3, 4], [0, -7, 9]):
    formal_sum = 0
    formal_product = 1
    for value in values:
        formal_sum += value
        formal_product *= value
    formal = (formal_sum, formal_product)
    print(
        f"values={values!r} formal={formal!r} "
        f"canonical={canonical(values)!r} candidate={candidate(values)!r}"
    )
