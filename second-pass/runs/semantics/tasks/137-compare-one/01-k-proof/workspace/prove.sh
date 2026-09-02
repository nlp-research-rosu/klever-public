#!/usr/bin/env bash
set -euo pipefail

# Translate the submitted implementation.
python3 py2mpy.py solution.py > solution.mpy

# Build and exercise the supplied concrete semantics.
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete.mpy --definition runtime-kompiled

# Build the symbolic proof definition without importing MPY-CONCRETE, then
# prove all nine int/float/string input-pair claims in one positive command.
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
