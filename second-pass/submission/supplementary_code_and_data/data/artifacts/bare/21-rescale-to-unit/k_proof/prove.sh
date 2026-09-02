#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy
python3 -c 'from solution import rescale_to_unit; assert rescale_to_unit([1.0, 2.0, 3.0, 4.0, 5.0]) == [0.0, 0.25, 0.5, 0.75, 1.0]'

kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX

krun solution.mpy \
  --definition verification-kompiled \
  -cARGS='vlist(1, 2, 3, 4, 5)' \
  --output pretty

krun solution.mpy \
  --definition verification-kompiled \
  -cARGS='vlist(-5, 0, 5, 5)' \
  --output pretty

kprove spec.k --definition verification-kompiled
