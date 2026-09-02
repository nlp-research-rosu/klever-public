#!/usr/bin/env bash
set -euo pipefail

# Regenerate the submitted constructor term from the submitted Python source.
python3 py2mpy.py solution.py > solution.mpy

# Build the required concrete LLVM semantics and run executable assertions.
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
python3 py2mpy.py smoke.py > smoke.mpy
krun smoke.mpy --definition runtime-kompiled

# Build the symbolic definition from the supplied MPY semantics plus the
# task-local verification layer, then prove every claim in spec.k.
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
