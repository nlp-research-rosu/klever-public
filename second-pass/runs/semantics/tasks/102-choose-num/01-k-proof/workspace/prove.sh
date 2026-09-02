#!/usr/bin/env bash
set -euo pipefail

# Regenerate the required translation and the concrete assertion harness.
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete_tests.py > concrete_tests.mpy

# Exercise the translated implementation with the supplied concrete semantics.
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete_tests.mpy --definition runtime-kompiled

# Build the symbolic definition and prove every claim in the specification.
kompile verification.k \
  --backend haskell \
  --main-module CHOOSE-NUM-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module CHOOSE-NUM-SPEC
