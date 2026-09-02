#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy

kompile semantic.k \
  --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --backend llvm \
  -o semantic-kompiled

krun solution.mpy --definition semantic-kompiled \
  -cARGS='ListV(IntV(3), IntV(1), IntV(2), IntV(4), IntV(5))'
krun solution.mpy --definition semantic-kompiled \
  -cARGS='ListV(IntV(1), IntV(2), IntV(3))'
krun solution.mpy --definition semantic-kompiled \
  -cARGS='ListV()'
krun solution.mpy --definition semantic-kompiled \
  -cARGS='ListV(IntV(7))'

kompile verification.k \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION \
  --backend haskell \
  -o verification-kompiled

# Mechanically check that the proof macro expands to the exact parsed
# solution.mpy constructor tree.
cmp \
  <(kast solution.mpy --definition verification-kompiled \
      --module VERIFICATION --sort Pgm --expand-macros --output kore) \
  <(kast --expression solutionProgram --definition verification-kompiled \
      --module VERIFICATION --sort Pgm --expand-macros --output kore)

# This single positive target proves every claim in spec.k.
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
