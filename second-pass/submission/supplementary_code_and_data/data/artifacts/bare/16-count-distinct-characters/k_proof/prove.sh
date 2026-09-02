#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

# Recreate the required transliteration and sanity-check the Python program.
python3 py2mpy.py solution.py > solution.mpy
python3 -m py_compile solution.py
python3 - <<'PY'
from solution import count_distinct_characters

assert count_distinct_characters("xyzXYZ") == 3
assert count_distinct_characters("Jerry") == 4
assert count_distinct_characters("") == 0
assert count_distinct_characters("AaBb!") == 3
PY

# Build the executable and symbolic definition.
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX

# Exercise the translated program through the semantics.
krun solution.mpy --definition verification-kompiled -cINPUT='"xyzXYZ"'
krun solution.mpy --definition verification-kompiled -cINPUT='"Jerry"'
krun solution.mpy --definition verification-kompiled -cINPUT='""'
krun solution.mpy --definition verification-kompiled -cINPUT='"AaBb!"'

# Prove all claims in spec.k.  Success prints #Top and exits zero.
kprove spec.k --definition verification-kompiled --spec-module SPEC
