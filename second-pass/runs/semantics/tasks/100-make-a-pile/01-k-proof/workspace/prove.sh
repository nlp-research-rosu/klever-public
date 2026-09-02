#!/usr/bin/env bash
set -euo pipefail

# Translate the submitted implementation with the fixed front end.
python3 py2mpy.py solution.py > solution.mpy

# Build the required concrete LLVM semantics and exercise representative
# positive odd/even inputs, including the smallest allowed input.
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
python3 py2mpy.py concrete_tests.py > concrete_tests.mpy
krun concrete_tests.mpy --definition runtime-kompiled

# Build the symbolic definition from the supplied MPY modules plus the
# mathematical sequence and list lemmas in verification.k.
kompile verification.k \
  --backend haskell \
  --main-module PILE-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

# The two #Top results compose at the exact loop-entry configuration:
# public entry point -> initialized invariant -> returned progression.
kprove spec.k \
  --definition verification-kompiled \
  --spec-module PILE-PREFIX-SPEC
kprove spec.k \
  --definition verification-kompiled \
  --spec-module PILE-LOOP-SPEC
