#!/usr/bin/env bash
set -euo pipefail

# Recreate the required translation from the submitted Python source.
python3 py2mpy.py solution.py > solution.mpy

# Concrete LLVM execution of the submitted module and four behavioral tests.
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun solution.mpy --definition runtime-kompiled
python3 py2mpy.py smoke.py > smoke.mpy
krun smoke.mpy --definition runtime-kompiled

# Symbolic definition and the required positive target proof.
kompile verification.k \
  --backend haskell \
  --main-module MAD-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module MAD-SPEC
