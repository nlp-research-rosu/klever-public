#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete-tests.py > concrete-tests.mpy
python3 concrete-tests.py

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete-tests.mpy --definition runtime-kompiled

kompile verification.k \
  --backend haskell \
  --main-module FIX-SPACES-BASE \
  --syntax-module MPY-SYNTAX \
  --output-definition proof-base-kompiled
kprove spec.k \
  --definition proof-base-kompiled \
  --spec-module FIX-SPACES-FLUSH-SPEC

kompile verification.k \
  --backend haskell \
  --main-module FIX-SPACES-FLUSH-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition proof-step-kompiled
kprove spec.k \
  --definition proof-step-kompiled \
  --spec-module FIX-SPACES-STEP-SPEC

kompile verification.k \
  --backend haskell \
  --main-module FIX-SPACES-STEP-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition proof-loop-kompiled
kprove spec.k \
  --definition proof-loop-kompiled \
  --spec-module FIX-SPACES-LOOP-SPEC

kompile verification.k \
  --backend haskell \
  --main-module FIX-SPACES-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition proof-main-kompiled
kprove spec.k \
  --definition proof-main-kompiled \
  --spec-module FIX-SPACES-MAIN-SPEC
