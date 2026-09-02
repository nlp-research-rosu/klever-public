#!/usr/bin/env bash
set -euo pipefail

cd -- "$(dirname -- "$0")"

# Recreate the translator artifact from the submitted Python implementation.
python3 py2mpy.py solution.py > solution.mpy

# Check the implementation under CPython as an independent executable sanity
# check before invoking the K model.
python3 - <<'PY'
from solution import sort_numbers

assert sort_numbers("three one five") == "one three five"
assert sort_numbers("two two one zero two") == "zero one two two two"
assert sort_numbers(
    "nine eight seven six five four three two one zero"
) == "zero one two three four five six seven eight nine"
assert sort_numbers("") == ""
PY

# Compile the semantics together with its proof-only verification functions.
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX

# Execute the actual translator output, not the compact proof abbreviation.
krun solution.mpy --definition verification-kompiled \
  -cARG='"three one five"'
krun solution.mpy --definition verification-kompiled \
  -cARG='"two two one zero two"'
krun solution.mpy --definition verification-kompiled \
  -cARG='"nine eight seven six five four three two one zero"'
krun solution.mpy --definition verification-kompiled -cARG='""'

# This single invocation proves every claim in spec.k and must print #Top.
kprove spec.k --definition verification-kompiled
