#!/usr/bin/env python3
import importlib.util

spec = importlib.util.spec_from_file_location("submitted_gap", "/candidate/solution.py")
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)

result = module.closest_integer("1e2")
print(f'candidate_CPythons_closest_integer("1e2")={result}')
assert result == 100
