#!/usr/bin/env bash
set -euo pipefail

# Recreate the constructor tree from the submitted Python source.
python3 py2mpy.py solution.py > solution.mpy

# Compile the executable semantics and exercise every example from prompt.py.
kompile semantic.k --backend haskell --main-module MPY --syntax-module MPY-SYNTAX
krun solution.mpy --definition semantic-kompiled -cN=5 --output pretty
krun solution.mpy --definition semantic-kompiled -cN=11 --output pretty
krun solution.mpy --definition semantic-kompiled -cN=0 --output pretty
krun solution.mpy --definition semantic-kompiled -cN=20 --output pretty
krun solution.mpy --definition semantic-kompiled -cN=1 --output pretty
krun solution.mpy --definition semantic-kompiled -cN=18 --output pretty

# Compile the independent mathematical reference definitions and prove all
# three claims: the divisor invariant, the candidate invariant, and the
# end-to-end result for every non-negative integer n.
kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX
kprove spec.k --definition verification-kompiled --spec-module SPEC --output pretty
