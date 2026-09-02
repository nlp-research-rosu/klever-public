#!/usr/bin/env bash
set -euo pipefail

# Recreate the submitted constructor term from the immutable translator.
python3 py2mpy.py solution.py > solution.mpy

# Compile and concretely exercise the translated program with our semantics.
kompile semantic.k \
  --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --backend llvm
krun solution.mpy -cN=5 --definition semantic-kompiled --output pretty
krun solution.mpy -cN=27 --definition semantic-kompiled --output pretty

# Compile the same semantics plus proof-only definitions, then prove all claims.
kompile verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --backend haskell
kprove spec.k --definition verification-kompiled --output pretty
