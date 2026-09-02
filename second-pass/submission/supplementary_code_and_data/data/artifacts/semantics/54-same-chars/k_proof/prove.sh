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

kompile verification.k \
  --backend haskell \
  --main-module SAME-CHARS-VERIFICATION \
  --syntax-module SAME-CHARS-VERIFICATION \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SAME-CHARS-SPEC
