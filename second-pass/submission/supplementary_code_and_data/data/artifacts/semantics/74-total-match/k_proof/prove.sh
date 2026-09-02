#!/usr/bin/env bash
set -euo pipefail

# Translate the submitted implementation.
python3 py2mpy.py solution.py > solution.mpy

# Concrete execution of all five examples from prompt.py.
python3 py2mpy.py concrete-tests.py > concrete-tests.mpy
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete-tests.mpy \
  --definition runtime-kompiled \
  --output none

# Symbolic definition: MPY excludes the concrete-only execution extensions.
kompile verification.k \
  --backend haskell \
  --main-module TOTAL-MATCH-VERIFICATION \
  --syntax-module TOTAL-MATCH-VERIFICATION \
  --output-definition verification-kompiled

# Prove the recursive loop invariant, then both end-to-end result claims.
kprove spec.k \
  --definition verification-kompiled \
  --spec-module TOTAL-MATCH-LOOP-SPEC
kprove spec.k \
  --definition verification-kompiled \
  --spec-module TOTAL-MATCH-SPEC
