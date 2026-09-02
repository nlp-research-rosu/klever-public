#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

# Recreate the K constructor term from the submitted Python implementation.
python3 py2mpy.py solution.py > solution.mpy

# Compile and exercise the standalone semantics on examples and edge cases.
kompile semantic.k --main-module MPY --syntax-module MPY-SYNTAX --backend haskell
krun solution.mpy --definition semantic-kompiled -cARG='pyStr("10")'
krun solution.mpy --definition semantic-kompiled -cARG='pyStr("15.3")'
krun solution.mpy --definition semantic-kompiled -cARG='pyStr("14.5")'
krun solution.mpy --definition semantic-kompiled -cARG='pyStr("-14.5")'
krun solution.mpy --definition semantic-kompiled -cARG='pyStr("-0.49")'
krun solution.mpy --definition semantic-kompiled -cARG='pyStr("-0.51")'
krun solution.mpy --definition semantic-kompiled -cARG='pyStr("1.499999999999999999999999")'
krun solution.mpy --definition semantic-kompiled -cARG='pyStr("1.500000000000000000000001")'
krun solution.mpy --definition semantic-kompiled -cARG='pyStr("1.5e2")'

# Compile the verification extension and prove every claim in spec.k.
kompile verification.k --main-module VERIFICATION --syntax-module MPY-SYNTAX --backend haskell
kprove spec.k --definition verification-kompiled --spec-module SPEC
