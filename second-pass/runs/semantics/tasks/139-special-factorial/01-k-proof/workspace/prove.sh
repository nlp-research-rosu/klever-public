#!/usr/bin/env bash
set -euo pipefail

# Translate the submitted implementation and the concrete known-answer driver.
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py run.py > run.mpy

# Build and exercise the supplied concrete semantics.
rm -rf -- ./runtime-kompiled
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun run.mpy --definition runtime-kompiled --output pretty

# Build the symbolic definition without importing MPY-CONCRETE, then prove
# both the inductive loop invariant and whole-program correctness claim.
rm -rf -- ./verification-kompiled
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --output pretty
