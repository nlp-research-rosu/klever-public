#!/usr/bin/env bash
set -euo pipefail

# Recreate the pure AST translation consumed by the semantics.
python3 py2mpy.py solution.py > solution.mpy

# Build an executable definition and run all examples from the prompt.
kompile semantic.k \
  --main-module MPY-SEMANTICS \
  --syntax-module MPY-SYNTAX \
  --backend llvm \
  --output-definition semantic-llvm-kompiled
krun solution.mpy --definition semantic-llvm-kompiled \
  -cARGS='ListVal(1, 2, 3)'
krun solution.mpy --definition semantic-llvm-kompiled \
  -cARGS='ListVal(.Ints)'
krun solution.mpy --definition semantic-llvm-kompiled \
  -cARGS='ListVal(-1, -5, 2, -1, -5)'

# Include the independent contract functions in the Haskell definition, then
# prove every claim in MPY-SPEC.  Success prints #Top and exits zero.
kompile verification.k \
  --main-module MPY-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --backend haskell \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module MPY-SPEC
