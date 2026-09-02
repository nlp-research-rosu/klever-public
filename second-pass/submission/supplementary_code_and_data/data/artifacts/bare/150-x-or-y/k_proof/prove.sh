#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

# Regenerate the constructor term with the fixed translator.
python3 py2mpy.py solution.py > solution.mpy

# Concrete execution uses the LLVM backend.
kompile semantic.k \
  --backend llvm \
  --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition llvm-kompiled

krun solution.mpy --definition llvm-kompiled -cN=7 -cX=34 -cY=12
krun solution.mpy --definition llvm-kompiled -cN=15 -cX=8 -cY=5
krun solution.mpy --definition llvm-kompiled -cN=97 -cX=11 -cY=22
krun solution.mpy --definition llvm-kompiled -cN=121 -cX=11 -cY=22

# Symbolic execution and reachability proofs use the Haskell backend.
kompile verification.k \
  --backend haskell \
  --main-module MPY-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

# First prove the generalized loop invariant, then use that proved claim to
# establish the universal entry-point theorem and both prompt examples.
kprove spec.k \
  --definition verification-kompiled \
  --spec-module LOOP-SPEC

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
