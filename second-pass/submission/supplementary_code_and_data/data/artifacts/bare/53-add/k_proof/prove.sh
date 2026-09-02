#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy
kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX
krun solution.mpy --definition verification-kompiled -cARG1=2 -cARG2=3
krun solution.mpy --definition verification-kompiled -cARG1=5 -cARG2=7
krun solution.mpy --definition verification-kompiled -cARG1=-8 -cARG2=3
kprove spec.k --definition verification-kompiled --spec-module SPEC
