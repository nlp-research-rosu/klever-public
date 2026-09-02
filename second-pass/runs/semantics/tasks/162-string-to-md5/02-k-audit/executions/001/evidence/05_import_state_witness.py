#!/usr/bin/env python3
"""Observable source-state witness for the semantics' no-op Import rule."""

import importlib.util
from pathlib import Path
import types

path = Path("/tmp/audit-work/proof-162/solution.py")
spec = importlib.util.spec_from_file_location("candidate_import_state", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

print(f"hashlib_in_module_globals={'hashlib' in vars(module)}")
print(f"hashlib_binding_type={type(vars(module)['hashlib']).__name__}")
print(f"is_module={isinstance(vars(module)['hashlib'], types.ModuleType)}")

assert "hashlib" in vars(module)
assert isinstance(vars(module)["hashlib"], types.ModuleType)
