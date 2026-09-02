#!/usr/bin/env bash
set -euo pipefail

# Recreate the translator artifacts from their Python sources.
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete_tests.py > concrete_tests.mpy

# Concrete execution uses the required LLVM main and syntax modules.
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete_tests.mpy --definition runtime-kompiled

# Symbolic proofs import MPY through verification.k and prove every claim in
# spec.k in one invocation.  Success is exactly exit status 0 plus #Top.
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
