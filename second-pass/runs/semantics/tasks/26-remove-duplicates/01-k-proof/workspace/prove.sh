#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete-tests.py > concrete-tests.mpy

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun concrete-tests.mpy \
  --definition runtime-kompiled \
  --output none

kompile verification.k \
  --backend haskell \
  --main-module REMOVE-DUPLICATES-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

# First prove the reusable loop invariant by circularity.
kprove spec.k \
  --definition verification-kompiled \
  --spec-module REMOVE-DUPLICATES-SPEC \
  --claims REMOVE-DUPLICATES-SPEC.loop-invariant \
  --output pretty

# Then use that already-proved invariant as a lemma for all entry cases.
kprove spec.k \
  --definition verification-kompiled \
  --spec-module REMOVE-DUPLICATES-SPEC \
  --trusted REMOVE-DUPLICATES-SPEC.loop-invariant \
  --output pretty
