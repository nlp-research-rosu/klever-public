#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy

kompile semantic.k \
  --backend haskell \
  --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX

krun solution.mpy --definition semantic-kompiled \
  -cARGS='args(5, 6, 10)'
krun solution.mpy --definition semantic-kompiled \
  -cARGS='args(4, 8, 9)'
krun solution.mpy --definition semantic-kompiled \
  -cARGS='args(1, 10, 10)'
krun solution.mpy --definition semantic-kompiled \
  -cARGS='args(2, 11, 5)'

kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX

kprove spec.k --definition verification-kompiled
