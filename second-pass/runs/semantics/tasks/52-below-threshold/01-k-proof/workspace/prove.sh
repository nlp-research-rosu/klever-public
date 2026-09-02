#!/usr/bin/env bash
set -euo pipefail

# Translate the submitted implementation and the concrete assertion harness.
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete-tests.py > concrete-tests.mpy

# Exercise the implementation through the supplied concrete LLVM semantics.
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete-tests.mpy \
  --definition runtime-kompiled \
  --output pretty

# First prove the recursive loop invariant against unextended MPY.
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION-BASE \
  --syntax-module VERIFICATION-BASE \
  --output-definition verification-base-kompiled
kprove spec.k \
  --definition verification-base-kompiled \
  --spec-module LOOP-SPEC \
  --output pretty

# Then admit that proved invariant verbatim as a derived rule and prove the
# complete translated function call against its mathematical contract.
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --output pretty
