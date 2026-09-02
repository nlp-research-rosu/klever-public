#!/usr/bin/env python3
"""Concrete false-conclusion witness for methods.k's broad encode identity."""

import hashlib
import importlib.util
from pathlib import Path

solution_path = Path("/tmp/audit-work/proof-162/solution.py")
spec = importlib.util.spec_from_file_location("candidate_solution", solution_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

text = "é"
code_points = [ord(character) for character in text]
utf8_bytes = list(text.encode("utf-8"))
identity_bytes = bytes(code_points)
actual = module.string_to_md5(text)
utf8_digest = hashlib.md5(bytes(utf8_bytes)).hexdigest()
identity_digest = hashlib.md5(identity_bytes).hexdigest()

print(f"text={text!r}")
print(f"code_points={code_points}")
print(f"utf8_bytes={utf8_bytes}")
print(f"candidate_actual={actual}")
print(f"md5_utf8_bytes={utf8_digest}")
print(f"md5_identity_code_bytes={identity_digest}")
print(f"digests_equal={utf8_digest == identity_digest}")

assert actual == utf8_digest
assert code_points != utf8_bytes
assert utf8_digest != identity_digest
