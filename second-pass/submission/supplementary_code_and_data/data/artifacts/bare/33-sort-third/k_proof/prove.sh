#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy

kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX

krun solution.mpy \
  --definition verification-kompiled \
  -cINPUT='VList(1, 2, 3)'

krun solution.mpy \
  --definition verification-kompiled \
  -cINPUT='VList(5, 6, 3, 4, 8, 9, 2)'

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
