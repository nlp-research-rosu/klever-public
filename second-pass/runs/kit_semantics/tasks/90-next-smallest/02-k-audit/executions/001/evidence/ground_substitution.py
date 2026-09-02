#!/usr/bin/env python3
import importlib.util
from pathlib import Path


def load(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, Path(path))
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.next_smallest


candidate = load("/tmp/audit-work/review-90/solution.py", "ground_candidate")
canonical = load("/tmp/audit-work/review-90/canonical.py", "ground_canonical")
for values, formal_result in [([3, 1, 2], 2), ([1, 1], None)]:
    generated_result = candidate(list(values))
    canonical_result = canonical(list(values))
    print(
        f"input={values!r} formal={formal_result!r} "
        f"generated={generated_result!r} canonical={canonical_result!r}"
    )
    assert generated_result == canonical_result == formal_result
