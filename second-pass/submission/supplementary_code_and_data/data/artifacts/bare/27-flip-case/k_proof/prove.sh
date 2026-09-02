#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy
python3 gen_unicode_case.py

kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX

krun solution.mpy \
  --definition verification-kompiled \
  -cARG='"Hello"'

krun solution.mpy \
  --definition verification-kompiled \
  -cARG='"Stra\u00dfe \u0394elta"'

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
