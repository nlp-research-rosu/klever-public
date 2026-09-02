#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete-tests.py > concrete-tests.mpy

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun concrete-tests.mpy --definition runtime-kompiled

kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION \
  --output-definition verification-kompiled

kprove \
  --definition verification-kompiled \
  spec.k \
  --spec-module LOOP-SPEC

kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION-WITH-LOOP \
  --syntax-module VERIFICATION-WITH-LOOP \
  --output-definition function-verification-kompiled

kprove \
  --definition function-verification-kompiled \
  spec.k \
  --spec-module FUNCTION-SPEC
