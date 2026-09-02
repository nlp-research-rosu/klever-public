#!/usr/bin/env python3
"""Mechanical whitespace-insensitive comparison of .mpy and entry-claim term."""

from pathlib import Path


mpy = Path("/tmp/audit-work/src/solution.mpy").read_text()
spec = Path("/tmp/audit-work/src/spec.k").read_text()
needle = "Module("
start = spec.index(needle, spec.index("largest-divisor-natural-contract"))

depth = 0
in_string = False
escaped = False
end = None
for index in range(start, len(spec)):
    char = spec[index]
    if in_string:
        if escaped:
            escaped = False
        elif char == "\\":
            escaped = True
        elif char == '"':
            in_string = False
        continue
    if char == '"':
        in_string = True
    elif char == "(":
        depth += 1
    elif char == ")":
        depth -= 1
        if depth == 0:
            end = index + 1
            break

assert end is not None
claim_term = spec[start:end]
normalize = lambda text: "".join(text.split())
equal = normalize(mpy) == normalize(claim_term)

print(f"mpy_chars={len(mpy)}")
print(f"claim_term_chars={len(claim_term)}")
print(f"normalized_equal={equal}")
print(f"mpy_normalized={normalize(mpy)}")
print(f"claim_normalized={normalize(claim_term)}")
raise SystemExit(0 if equal else 1)
