#!/usr/bin/env bash
set -euo pipefail

# Regenerate the constructor term from the submitted Python implementation.
python3 py2mpy.py solution.py > solution.mpy

# Check the prompt examples and two boundary cases in CPython.
python3 - <<'PY'
from solution import below_threshold

assert below_threshold([1, 2, 4, 10], 100) is True
assert below_threshold([1, 20, 4, 10], 5) is False
assert below_threshold([], -100) is True
assert below_threshold([5], 5) is False
print("CPython tests: passed")
PY

# Compile the handwritten semantics together with the verification helpers.
kompile verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --backend haskell

# Exercise the translated program through the semantics.
krun solution.mpy --definition verification-kompiled \
  -cINPUT='cons(1, cons(2, cons(4, cons(10, nil))))' \
  -cTHRESHOLD=100
krun solution.mpy --definition verification-kompiled \
  -cINPUT='cons(1, cons(20, cons(4, cons(10, nil))))' \
  -cTHRESHOLD=5
krun solution.mpy --definition verification-kompiled \
  -cINPUT='nil' \
  -cTHRESHOLD=-100
krun solution.mpy --definition verification-kompiled \
  -cINPUT='cons(5, nil)' \
  -cTHRESHOLD=5

# Prove every claim in spec.k; success prints #Top and exits zero.
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --output pretty
