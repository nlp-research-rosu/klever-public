#!/usr/bin/env python3
import importlib.util
from pathlib import Path


path = Path("/tmp/audit-work/reconstruction/solution.py")
spec = importlib.util.spec_from_file_location("generated_solution", path)
assert spec is not None and spec.loader is not None
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
result = module.compare_one("1e2", 500.0)
print(f"generated_path={path}")
print("input=('1e2', 500.0)")
print(f"generated_result={result!r}")
assert result == 500.0
