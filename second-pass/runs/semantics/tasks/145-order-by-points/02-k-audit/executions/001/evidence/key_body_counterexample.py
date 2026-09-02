#!/usr/bin/env python3
"""Ground witness for the key-body sensitivity failure."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


def load(path: Path):
    spec = spec_from_file_location(path.stem, path)
    assert spec is not None and spec.loader is not None
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load(Path("/reference/canonical.py"))
values = [11, 1]


def wrong_digit_sum(_value: int) -> int:
    return 0


expected = canonical.order_by_points(values)
wrong_key_result = sorted(values, key=wrong_digit_sum)

print(f"input={values}")
print(f"canonical_result={expected}")
print(f"wrong_key_result={wrong_key_result}")
print(f"false_natural_conclusion={wrong_key_result != expected}")

raise SystemExit(0 if wrong_key_result != expected else 1)
