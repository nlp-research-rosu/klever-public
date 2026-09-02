#!/usr/bin/env bash
set -euo pipefail

python3 -m py_compile solution.py
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete_tests.py > concrete-tests.mpy

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun concrete-tests.mpy \
  --definition runtime-kompiled \
  --output pretty

kompile verification.k \
  --backend haskell \
  --main-module EXCHANGE-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification9-kompiled

kprove spec.k \
  --definition verification9-kompiled \
  --spec-module EXCHANGE-SPEC \
  --output pretty
