#!/usr/bin/env bash
set -euo pipefail

# Translate the submitted implementation with the fixed frontend.
python3 py2mpy.py solution.py > solution.mpy

# Concrete execution uses exactly the required LLVM modules.
python3 py2mpy.py concrete_tests.py > concrete_tests.mpy
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete_tests.mpy --definition runtime-kompiled

# Symbolic verification imports MPY, without the concrete-only MPY-CONCRETE leg.
kompile verification.k \
  --backend haskell \
  --main-module SELECT-WORDS-VERIFICATION \
  --syntax-module SELECT-WORDS-VERIFICATION \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SELECT-WORDS-SPEC
