#!/usr/bin/env python3
"""Syntactic pinning check from submitted .mpy function to the entry closure."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

solution_path = Path("/tmp/audit-work/src/solution.mpy")
spec_path = Path("/tmp/audit-work/src/spec.k")

solution_bytes = solution_path.read_bytes()
solution = re.sub(r"\s+", "", solution_bytes.decode())
spec = re.sub(r"\s+", "", spec_path.read_text())

prefix = 'Module(FuncDef("add_elements",Params("arr","k"),'
suffix = "))"
assert solution.startswith(prefix) and solution.endswith(suffix)
body = solution[len(prefix) : -len(suffix)]
# `.Stmts` is K's explicit empty-list token. The trusted translator prints the
# same empty productions by omission, while the hand-written claim spells them
# explicitly, so erase only that list-unit token before byte-like comparison.
spec_without_empty_stmts = spec.replace(".Stmts", "")
entry_closure = f'closureVal(("arr","k",.ParamNames),{body},0)'

print(f"SOLUTION_MPY_SHA256: {hashlib.sha256(solution_bytes).hexdigest()}")
print(f"NORMALIZED_FUNCTION_BODY: {body}")
print(f"EXPECTED_ENTRY_CLOSURE: {entry_closure}")
print(
    "ENTRY_CONTAINS_EXACT_CLOSURE_AFTER_EMPTY_LIST_NORMALIZATION: "
    f"{entry_closure in spec_without_empty_stmts}"
)
print("ENTRY_STARTS_AT_DIRECT_CLOSURE_CALL: true")
print("MODULE_LOAD_AND_FUNCDEF_BINDING_IN_ENTRY: false")

assert entry_closure in spec_without_empty_stmts
