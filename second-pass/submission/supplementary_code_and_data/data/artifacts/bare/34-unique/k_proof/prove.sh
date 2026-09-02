#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy
kompile verification.k --main-module VERIFICATION --syntax-module MPY-SYNTAX --backend haskell

krun solution.mpy --definition verification-kompiled -cARGS='ListExpr(Int(5), Int(3), Int(5), Int(2), Int(3), Int(3), Int(9), Int(0), Int(123))'
krun solution.mpy --definition verification-kompiled -cARGS='ListExpr()'
krun solution.mpy --definition verification-kompiled -cARGS='ListExpr(Int(-1), Int(-1), Int(2), Int(0))'

kprove spec.k --definition verification-kompiled --spec-module SPEC
