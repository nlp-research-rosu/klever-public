#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy

kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX

krun solution.mpy \
  --definition verification-kompiled \
  -cINPUT='ListExpr(Int(2), Int(4), Int(1), Int(3), Int(5), Int(7))'
krun solution.mpy \
  --definition verification-kompiled \
  -cINPUT='ListExpr()'
krun solution.mpy \
  --definition verification-kompiled \
  -cINPUT='ListExpr(Int(0))'
krun solution.mpy \
  --definition verification-kompiled \
  -cINPUT='ListExpr(Int(-6), Int(-1), Int(-9), Int(4), Int(2))'

kprove spec.k --definition verification-kompiled
