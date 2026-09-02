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
  --main-module HUMAN-EVAL-118-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition proof-kompiled

kprove spec.k \
  --definition proof-kompiled \
  --spec-module HUMAN-EVAL-118-SPEC
