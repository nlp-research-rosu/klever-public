#!/usr/bin/env python3
"""Append ground assertions to an exact byte copy of candidate solution.py."""

from __future__ import annotations

import hashlib
from pathlib import Path


source_path = Path("/candidate/solution.py")
target_path = Path("/tmp/audit-work/reconstruction/audit-concrete-harness.py")
source = source_path.read_bytes()
assert source.endswith(b"\n")
assertions = b"""

assert separate_paren_groups("") == []
assert separate_paren_groups("   ") == []
assert separate_paren_groups("()") == ["()"]
assert separate_paren_groups("(())") == ["(())"]
assert separate_paren_groups("() (())") == ["()", "(())"]
assert separate_paren_groups("( ) (( )) (( )( ))") == ["()", "(())", "(()())"]
"""
target_path.write_bytes(source + assertions)
round_trip = target_path.read_bytes()
assert round_trip[: len(source)] == source
print(f"SOURCE_PREFIX_BYTES={len(source)}")
print(f"SOURCE_PREFIX_SHA256={hashlib.sha256(source).hexdigest()}")
print(f"HARNESS_PATH={target_path}")
print("SOURCE_PREFIX_BYTE_IDENTICAL=True")
