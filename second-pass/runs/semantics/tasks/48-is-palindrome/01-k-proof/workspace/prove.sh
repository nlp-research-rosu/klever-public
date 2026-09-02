#!/usr/bin/env bash
set -euo pipefail

# Translate the submitted implementation with the fixed front end.
python3 py2mpy.py solution.py > solution.mpy

# Compile and run concrete assertions through the required LLVM semantics.
python3 py2mpy.py concrete-tests.py > concrete-tests.mpy
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete-tests.mpy --definition runtime-kompiled

# Compile the symbolic extension without the concrete-only module, then prove
# every claim in SPEC. Successful proof output is exactly #Top (plus warnings).
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
