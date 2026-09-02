#!/usr/bin/env bash
set -euo pipefail

# Translate the delivered implementation and the concrete assertion harness.
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete-tests.py > concrete-tests.mpy

# Required concrete LLVM definition and K-level execution.
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete-tests.mpy \
  --definition runtime-kompiled \
  --output pretty \
  --statistics

# Symbolic definition: VERIFICATION imports MPY, not MPY-CONCRETE.
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

# Positive target proof: success is "#Top" with exit status 0.
kprove spec.k \
  --definition verification-kompiled \
  --output pretty
