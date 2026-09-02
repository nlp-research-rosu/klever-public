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
  --main-module ANTI-SHUFFLE-BASE \
  --syntax-module MPY-SYNTAX \
  --output-definition word-verification-kompiled

kprove spec.k \
  --definition word-verification-kompiled \
  --spec-module WORD-SPEC

kompile verification.k \
  --backend haskell \
  --main-module ANTI-SHUFFLE-LOOP-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition loop-verification-kompiled

kprove spec.k \
  --definition loop-verification-kompiled \
  --spec-module ANTI-LOOP-SPEC

kompile verification.k \
  --backend haskell \
  --main-module ANTI-SHUFFLE-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module ANTI-SHUFFLE-SPEC
