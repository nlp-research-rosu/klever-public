#!/usr/bin/env bash
set -euo pipefail

# Translate the submitted Python implementation.
python3 py2mpy.py solution.py > solution.mpy

# Build the supplied concrete semantics exactly as required, then run all
# examples from prompt.py as assertions.
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled \
  -w none
krun concrete-tests.mpy --definition runtime-kompiled

# Build the symbolic extension (which imports MPY, not MPY-KRUN) and prove
# every reachability claim in spec.k.
kompile verification.k \
  --backend haskell \
  --main-module MODP-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled \
  -w none
kprove spec.k \
  --definition verification-kompiled \
  --spec-module MODP-SPEC \
  -w none
