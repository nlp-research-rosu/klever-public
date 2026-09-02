#!/usr/bin/env python3
"""Build a concrete K test program by appending calls to the exact candidate source."""

from pathlib import Path

CANDIDATE = Path("/tmp/audit-work/50-decode-shift/candidate-src/solution.py")
HARNESS = Path("/tmp/audit-work/50-decode-shift/concrete_harness.py")

candidate_text = CANDIDATE.read_text(encoding="utf-8")
tests = """

assert decode_shift("") == ""
assert decode_shift("e") == "z"
assert decode_shift("f") == "a"
assert decode_shift("mjqqt") == "hello"
assert decode_shift("fghijklmnopqrstuvwxyzabcde") == "abcdefghijklmnopqrstuvwxyz"
"""
HARNESS.write_text(candidate_text + tests, encoding="utf-8")

roundtrip_prefix = HARNESS.read_text(encoding="utf-8")[: len(candidate_text)]
if roundtrip_prefix != candidate_text:
    raise SystemExit("harness prefix does not exactly match candidate solution.py")

print(f"candidate_source_bytes={len(candidate_text.encode('utf-8'))}")
print(f"harness_prefix_byte_identity={roundtrip_prefix == candidate_text}")
print("cases=['', 'e', 'f', 'mjqqt', 'fghijklmnopqrstuvwxyzabcde']")
