#!/usr/bin/env bash
set -euo pipefail

# Translation and concrete regression program.
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete-tests.py > concrete-tests.mpy

# Concrete execution uses the required LLVM/main/syntax modules.
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun solution.mpy \
  --definition runtime-kompiled \
  --output pretty
krun concrete-tests.mpy \
  --definition runtime-kompiled \
  --output pretty

# First prove the generalized, continuation-parametric loop invariant using
# only MPY plus the proof vocabulary in SUM-PRODUCT-VERIFICATION.
kompile verification.k \
  --backend haskell \
  --main-module SUM-PRODUCT-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SUM-PRODUCT-LOOP-SPEC \
  --output pretty

# Promote that proved statement to the staged lemma module, then prove the
# end-to-end claim over the exact solution module.
kompile verification.k \
  --backend haskell \
  --main-module SUM-PRODUCT-LEMMA \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-lemma-kompiled
kprove spec.k \
  --definition verification-lemma-kompiled \
  --spec-module SUM-PRODUCT-FUNCTION-SPEC \
  --output pretty
