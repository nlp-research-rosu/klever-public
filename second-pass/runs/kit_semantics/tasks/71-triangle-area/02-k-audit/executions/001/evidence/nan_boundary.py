#!/usr/bin/env python3
import importlib.util
import math


spec = importlib.util.spec_from_file_location(
    "nan_candidate", "/tmp/audit-work/proof/solution.py"
)
assert spec is not None and spec.loader is not None
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

result = module.triangle_area(float("nan"), 3.0, 4.0)
print(f"CPYTHON_IS_NAN={math.isnan(result)}")
print(f"CPYTHON_RESULT={result!r}")
assert math.isnan(result)
