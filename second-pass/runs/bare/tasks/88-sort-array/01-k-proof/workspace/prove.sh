#!/usr/bin/env bash
set -euo pipefail

# Recreate the exact constructor term from the submitted Python source.
python3 py2mpy.py solution.py > solution.mpy

# Check the prompt examples in CPython and assert the non-mutation clause.
python3 - <<'PY'
from solution import sort_array

cases = [
    ([], []),
    ([5], [5]),
    ([2, 4, 3, 0, 1, 5], [0, 1, 2, 3, 4, 5]),
    ([2, 4, 3, 0, 1, 5, 6], [6, 5, 4, 3, 2, 1, 0]),
]
for source, expected in cases:
    before = source.copy()
    result = sort_array(source)
    assert result == expected
    assert source == before
    assert result is not source
PY

# Compile the semantics together with its executable verification observers.
kompile semantic.k \
  --backend haskell \
  --main-module MPY-VERIFICATION \
  --syntax-module MPY-SYNTAX

# Exercise all prompt examples through the semantics.
krun solution.mpy -d semantic-kompiled -cINPUT='nil'
krun solution.mpy -d semantic-kompiled -cINPUT='cons(5, nil)'
krun solution.mpy -d semantic-kompiled \
  -cINPUT='cons(2, cons(4, cons(3, cons(0, cons(1, cons(5, nil))))))'
krun solution.mpy -d semantic-kompiled \
  -cINPUT='cons(2, cons(4, cons(3, cons(0, cons(1, cons(5, cons(6, nil)))))))'

# This single positive target command proves every claim in SPEC.  pipefail
# preserves kprove's status, and the final check requires its success marker.
proof_output="$(mktemp)"
trap 'rm -f "$proof_output"' EXIT
kprove spec.k --definition semantic-kompiled --spec-module SPEC | tee "$proof_output"
grep -qx '#Top' "$proof_output"
