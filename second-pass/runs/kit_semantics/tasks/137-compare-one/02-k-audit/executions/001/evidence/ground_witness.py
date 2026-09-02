#!/usr/bin/env python3
import importlib.util
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.compare_one


a, b = 1, 2
generated = load(Path("/tmp/audit-work/reconstruction/solution.py"), "generated")
canonical = load(Path("/reference/canonical.py"), "canonical")
print("input=(1, 2)")
print("formal_claim=SPEC.int-int")
print("formal_expectedCompare(1,2)=2 because 1 > 2 is false and 2 > 1 is true")
print(f"generated_result={generated(a, b)!r}")
print(f"canonical_result={canonical(a, b)!r}")
assert generated(a, b) == canonical(a, b) == 2
