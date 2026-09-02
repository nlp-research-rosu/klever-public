#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy
python3 - <<'PY'
from solution import modp

assert modp(3, 5) == 3
assert modp(1101, 101) == 2
assert modp(0, 101) == 1
assert modp(3, 11) == 8
assert modp(100, 101) == 1
PY

kompile verification.k \
  --backend haskell \
  --main-module MODP-VERIFICATION \
  --syntax-module MODP-SYNTAX

krun solution.mpy --definition verification-kompiled -cN=3 -cP=5
krun solution.mpy --definition verification-kompiled -cN=1101 -cP=101
krun solution.mpy --definition verification-kompiled -cN=0 -cP=101
krun solution.mpy --definition verification-kompiled -cN=3 -cP=11
krun solution.mpy --definition verification-kompiled -cN=100 -cP=101

kprove spec.k \
  --definition verification-kompiled \
  --spec-module MODP-SPEC
