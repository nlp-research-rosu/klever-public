#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

# Regenerate the constructor term from the submitted Python implementation.
python3 py2mpy.py solution.py > solution.mpy

# Concrete execution uses the LLVM definition built from our semantics.
kompile semantic.k \
  --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --backend llvm
krun solution.mpy --definition semantic-kompiled -cARGS='input(1,2,2,-4)'
krun solution.mpy --definition semantic-kompiled -cARGS='input(0,1)'
krun solution.mpy --definition semantic-kompiled -cARGS='input()'
krun solution.mpy --definition semantic-kompiled -cARGS='input(-1,-2,-3)'

# Symbolic proof uses the Haskell backend and must print #Top.
kompile verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --backend haskell
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
