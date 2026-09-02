#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete_tests.py > concrete_tests.mpy

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun concrete_tests.mpy \
  --definition runtime-kompiled \
  --output pretty

# First prove the generalized, self-circular loop theorem against only MPY
# and the proof-side bracket-string encoding.
kompile verification.k \
  --backend haskell \
  --main-module IS-NESTED-VERIFICATION \
  --syntax-module IS-NESTED-VERIFICATION \
  --output-definition verification-kompiled

kprove \
  --definition verification-kompiled \
  --spec-module IS-NESTED-LOOP-SPEC \
  spec.k

# Recompile with that proved theorem installed as a modular lemma, then prove
# both entry-point claims (including the universal bracket-string claim).
kompile verification.k \
  --backend haskell \
  --main-module IS-NESTED-VERIFICATION-WITH-LOOP-LEMMA \
  --syntax-module IS-NESTED-VERIFICATION \
  --output-definition verification-with-lemma-kompiled

kprove \
  --definition verification-with-lemma-kompiled \
  --spec-module IS-NESTED-TOP-SPEC \
  spec.k
