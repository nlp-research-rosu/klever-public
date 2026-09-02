#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy
python3 -m py_compile solution.py

kompile semantic.k \
  --backend haskell \
  --main-module MPY-SEMANTICS \
  --syntax-module MPY-SYNTAX

krun solution.mpy \
  -cINPUT='ListExpr(Int(1), Int(11), Int(-1), Int(-11), Int(-12))' \
  --definition semantic-kompiled
krun solution.mpy \
  -cINPUT='ListExpr()' \
  --definition semantic-kompiled
krun solution.mpy \
  -cINPUT='ListExpr(Int(12), Int(21), Int(-12), Int(3))' \
  --definition semantic-kompiled

kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
