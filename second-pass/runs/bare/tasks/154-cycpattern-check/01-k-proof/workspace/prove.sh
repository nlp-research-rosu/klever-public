#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy
diff -u solution.mpy <(python3 py2mpy.py solution.py)
python3 build_solution_k.py > solution-program.k

kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module VERIFICATION-SYNTAX

krun solution.mpy --definition verification-kompiled -cARGS='pyStr("abcd") pyStr("abd")'
krun solution.mpy --definition verification-kompiled -cARGS='pyStr("hello") pyStr("ell")'
krun solution.mpy --definition verification-kompiled -cARGS='pyStr("abab") pyStr("baa")'

kprove spec.k --definition verification-kompiled --spec-module SPEC
