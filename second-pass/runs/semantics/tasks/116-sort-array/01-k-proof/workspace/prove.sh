#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

python3 py2mpy.py concrete-tests.py > concrete-tests.mpy
krun concrete-tests.mpy --definition runtime-kompiled
python3 differential_test.py

kompile verification.k \
  --backend haskell \
  --main-module SORT-ARRAY-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SORT-ARRAY-SPEC
