#!/bin/sh
set -eu

python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete_tests.py > concrete_tests.mpy

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun concrete_tests.mpy --definition runtime-kompiled

kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION \
  --output-definition verification-kompiled

# First establish the reusable structural loop invariant.
kprove spec.k \
  --definition verification-kompiled \
  --claims loop-invariant

# Then prove the two exhaustive entry-point cases using that established lemma.
kprove spec.k \
  --definition verification-kompiled \
  --claims loop-invariant,entry-empty,entry-cons \
  --trusted loop-invariant
