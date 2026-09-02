#!/usr/bin/env bash
set -euo pipefail

# Translate the submitted implementation with the fixed front end.
python3 py2mpy.py solution.py > solution.mpy

# Build and run concrete assertions with the required LLVM main module.
python3 py2mpy.py concrete-tests.py > concrete-tests.mpy
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete-tests.mpy --definition runtime-kompiled

# Build the symbolic extension over MPY (not MPY-KRUN) and prove every claim.
kompile verification.k \
  --backend haskell \
  --main-module DOUBLE-THE-DIFFERENCE-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module DOUBLE-THE-DIFFERENCE-SPEC
