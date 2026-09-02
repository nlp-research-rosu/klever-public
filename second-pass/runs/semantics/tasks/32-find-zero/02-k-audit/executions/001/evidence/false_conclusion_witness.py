#!/usr/bin/env python3
"""Concrete values for the proof-local rules' false-conclusion witnesses."""

import importlib.util
from pathlib import Path


spec = importlib.util.spec_from_file_location("trusted_canonical", Path("/reference/canonical.py"))
if spec is None or spec.loader is None:
    raise RuntimeError("cannot import trusted canonical")
canonical = importlib.util.module_from_spec(spec)
spec.loader.exec_module(canonical)

xs = [1, 2]
begin, end = -1.0, 1.0
bracket_iterations = 0
while canonical.poly(xs, begin) * canonical.poly(xs, end) > 0:
    begin *= 2.0
    end *= 2.0
    bracket_iterations += 1

actual_result = canonical.find_zero(xs)

# No candidate equation constrains these program-derived symbols. This is an
# admissible opposite interpretation of the claimed mathematical summaries.
opposite_bracket_low = 42.0
opposite_bracket_high = 43.0
opposite_bisect_low = 42.0

print(f"intended_input={xs!r}")
print(f"fixed_bracket_iterations={bracket_iterations}")
print(f"fixed_bracket_state={(begin, end)!r}")
print(
    "admissible_opaque_interpretation="
    f"bracketLow:{opposite_bracket_low},"
    f"bracketHigh:{opposite_bracket_high},"
    f"bisectLow:{opposite_bisect_low}"
)
print(f"fixed_find_zero_result={actual_result!r}")
print(f"poly_at_opposite_bisectLow={canonical.poly(xs, opposite_bisect_low)!r}")
print("candidate_approximatesZero_conclusion=true")
