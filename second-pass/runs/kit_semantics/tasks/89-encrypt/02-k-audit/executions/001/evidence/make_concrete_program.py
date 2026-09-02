#!/usr/bin/env python3
"""Create a K-translatable concrete harness with the exact submitted function."""

from __future__ import annotations

import hashlib
from pathlib import Path


WORK = Path("/tmp/audit-work/reconstruction")
SOURCE = WORK / "solution.py"
OUTPUT = WORK / "concrete_audit.py"
EXPECTED = "e0a9154ebe9aa14876a98ae1104bfc0de52b324e7b916afba4cba0f3157d5ce7"

tests = r'''

assert encrypt("") == ""
assert encrypt("hi") == "lm"
assert encrypt("asdfghjkl") == "ewhjklnop"
assert encrypt("gf") == "kj"
assert encrypt("et") == "ix"
assert encrypt("`az{") == "`ed{"
assert encrypt("vwxyz") == "zabcd"
assert encrypt("VWXYZ") == "VWXYZ"
assert encrypt("a z!") == "e d!"
'''

source_bytes = SOURCE.read_bytes()
actual = hashlib.sha256(source_bytes).hexdigest()
assert actual == EXPECTED, (actual, EXPECTED)
OUTPUT.write_bytes(source_bytes + tests.encode("utf-8"))
assert OUTPUT.read_bytes().startswith(source_bytes)
print(f"submitted_solution_sha256={actual}")
print(f"concrete_harness={OUTPUT}")
print(f"exact_solution_prefix_bytes={len(source_bytes)}")
