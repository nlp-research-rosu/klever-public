#!/usr/bin/env python3
"""Exhibit and independently evaluate a satisfying ground entry state."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.fruit_distribution


text = "5 apples and 6 oranges"
total = 19
tokens = text.split()
apple_codes = tuple(map(ord, tokens[0]))
orange_codes = tuple(map(ord, tokens[3]))
apples = int(tokens[0])
oranges = int(tokens[3])
conditions = {
    "split_shape": tokens == ["5", "apples", "and", "6", "oranges"],
    "apple_nonempty": len(apple_codes) > 0,
    "orange_nonempty": len(orange_codes) > 0,
    "apple_ascii_digits": all(48 <= code <= 57 for code in apple_codes),
    "orange_ascii_digits": all(48 <= code <= 57 for code in orange_codes),
    "apple_parse": apples == 5,
    "orange_parse": oranges == 6,
    "nonnegative_counts": apples >= 0 and oranges >= 0,
    "consistent_total": total >= apples + oranges,
}
assert all(conditions.values())
expected = total - apples - oranges
canonical = load(Path("/reference/canonical.py"), "witness_canonical")
generated = load(Path("/candidate/solution.py"), "witness_generated")
canonical_result = canonical(text, total)
generated_result = generated(text, total)
assert expected == canonical_result == generated_result == 8
print(f"TEXT={text!r}")
print(f"CS={tuple(map(ord, text))}")
print(f"APPLECODES={apple_codes} ORANGECODES={orange_codes}")
for name, value in conditions.items():
    print(f"PRECONDITION {name}={value}")
print(
    f"POSTCONDITION 19-5-6={expected} "
    f"canonical={canonical_result} generated={generated_result}"
)
print("PRECONDITION_WITNESS=PASS")
