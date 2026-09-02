#!/usr/bin/env bash
set -euo pipefail

# Recreate the required translation from the submitted Python source.
python3 py2mpy.py solution.py > solution.mpy

# Compile the supplied semantics' concrete LLVM entry point and exercise the
# prompt examples plus edge cases.  Failed K assertions make krun exit nonzero.
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
python3 py2mpy.py concrete_tests.py > concrete-tests.mpy
krun concrete-tests.mpy --definition runtime-kompiled

# Compile the symbolic definition without MPY-CONCRETE, then prove every claim
# in spec.k.  Success prints #Top and exits zero.
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
