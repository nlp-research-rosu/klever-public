#!/usr/bin/env bash
set -euo pipefail

# Recreate the constructor program from the unmodified translator.
python3 py2mpy.py solution.py > solution.mpy

# Concrete execution definition and representative runs (including the prompt example).
kompile semantic.k \
  --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --backend llvm \
  --output-definition runtime-kompiled
krun solution.mpy --definition runtime-kompiled -cN=1
krun solution.mpy --definition runtime-kompiled -cN=5
krun solution.mpy --definition runtime-kompiled -cN=10

# The proof definition includes the independently named mathematical contract.
kompile verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --backend haskell \
  --output-definition verification-kompiled

# This is the sole positive target-proof command; it proves every claim in spec.k.
kprove spec.k --definition verification-kompiled
