#!/usr/bin/env bash
set -euo pipefail

cd -- "$(dirname -- "$0")"

python3 py2mpy.py solution.py > solution.mpy

kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX

krun solution.mpy \
  --definition verification-kompiled \
  -cARGS='nums(rat(1,1),rat(2,1),rat(3,1),rat(4,1))'

krun solution.mpy \
  --definition verification-kompiled \
  -cARGS='nums(rat(-2,1),rat(0,1),rat(2,1))'

kprove spec.k --definition verification-kompiled
