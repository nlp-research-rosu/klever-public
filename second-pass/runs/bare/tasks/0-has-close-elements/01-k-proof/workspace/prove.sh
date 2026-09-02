#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy

python3 - <<'PY'
from solution import has_close_elements

assert has_close_elements([1.0, 2.0, 3.0], 0.5) is False
assert has_close_elements([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3) is True
assert has_close_elements([], 1.0) is False
assert has_close_elements([1.0], 1.0) is False
assert has_close_elements([1.0, 1.5], 0.5) is False
assert has_close_elements([1.0, 1.5], 0.5000001) is True
PY

kompile semantic.k \
  --backend haskell \
  --main-module MPY \
  --syntax-module MPY-SYNTAX

run_example_one="$(krun solution.mpy \
  --definition semantic-kompiled \
  -cARGS='VList(VRat(10,10),VRat(20,10),VRat(30,10)),VRat(5,10)')"
printf '%s\n' "$run_example_one"
grep -q 'VBool ( false )' <<<"$run_example_one"

run_example_two="$(krun solution.mpy \
  --definition semantic-kompiled \
  -cARGS='VList(VRat(10,10),VRat(28,10),VRat(30,10),VRat(40,10),VRat(50,10),VRat(20,10)),VRat(3,10)')"
printf '%s\n' "$run_example_two"
grep -q 'VBool ( true )' <<<"$run_example_two"

kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX

kprove spec.k --definition verification-kompiled
