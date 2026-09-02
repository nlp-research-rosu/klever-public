#!/usr/bin/env bash
set -euo pipefail

# Regenerate the submitted constructor term with the fixed translator.
python3 py2mpy.py solution.py > solution.mpy
python3 -m py_compile solution.py concrete_tests.py

# Build and run the supplied concrete semantics.  The test program exercises
# all hypotenuse positions, ordinary false cases, and non-positive lengths.
python3 py2mpy.py concrete_tests.py > concrete-tests.mpy
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete-tests.mpy --definition runtime-kompiled

# Build the symbolic definition from the supplied MPY modules and prove every
# claim in spec.k.  Success is an exit status of zero and the output "#Top".
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
