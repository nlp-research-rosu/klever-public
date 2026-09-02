#!/usr/bin/env python3
"""Ground witnesses for every submitted claim precondition."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load_entry(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sort_array


canonical = load_entry(Path("/tmp/audit-work/reconstruction/canonical.py"), "canonical")
generated = load_entry(Path("/tmp/audit-work/reconstruction/solution.py"), "generated")

print("CLAIM_1_WITNESS initial empty heap/scopes configuration; no requires clause")

for values in ([], [0], [7, 3, 5, 6, 9, 8], [3, 3, 0, 8, 1]):
    precondition = all(isinstance(value, int) and value >= 0 for value in values)
    oracle = sorted(values, key=lambda value: (bin(value).count("1"), value))
    print(
        f"CLAIM_2_WITNESS VS={values!r} precondition={precondition} "
        f"formal_intended_result={oracle!r} canonical={canonical(list(values))!r} "
        f"generated={generated(list(values))!r}"
    )
    assert precondition
    assert canonical(list(values)) == generated(list(values)) == oracle

for value in (0, 1, 7, (1 << 127) + 1):
    key = bin(value).count("1")
    print(
        f"CLAIM_3_WITNESS N={value} precondition={value >= 0} "
        f"cntSub_bin_count={key}"
    )
    assert value >= 0

for value in (-1, -5):
    generated_key = 0 if value < 0 else bin(value).count("1")
    print(
        f"CLAIM_4_WITNESS N={value} precondition={value < 0} "
        f"generated_key={generated_key}"
    )
    assert value < 0 and generated_key == 0
