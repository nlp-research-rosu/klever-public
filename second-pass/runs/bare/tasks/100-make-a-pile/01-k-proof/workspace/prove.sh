#!/usr/bin/env bash
set -euo pipefail

# Regenerate the submitted constructor term from the submitted Python source.
python3 py2mpy.py solution.py > solution.mpy

# Build the executable small-step semantics and exercise representative inputs.
kompile semantic.k --backend llvm --main-module MPY --syntax-module MPY-SYNTAX
krun solution.mpy --definition semantic-kompiled -cN=1
krun solution.mpy --definition semantic-kompiled -cN=3
krun solution.mpy --definition semantic-kompiled -cN=6

# Build the proof definition, then prove every claim in spec.k.
kompile verification.k --backend haskell \
  --output-definition verification-kompiled \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX
kprove spec.k --definition verification-kompiled --spec-module SPEC
