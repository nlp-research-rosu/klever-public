#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py smoke.py > smoke.mpy

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun smoke.mpy \
  --definition runtime-kompiled \
  --output pretty

kompile verification.k \
  --backend haskell \
  --main-module IS-SORTED-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition loop-verification-kompiled

kprove spec.k \
  --definition loop-verification-kompiled \
  --spec-module IS-SORTED-LOOP-SPEC \
  --output pretty

kompile verification.k \
  --backend haskell \
  --main-module IS-SORTED-WITH-LOOP-LEMMA \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module IS-SORTED-SPEC \
  --output pretty
