#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete_tests.py > concrete_tests.mpy

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun solution.mpy \
  --definition runtime-kompiled \
  --output none

krun concrete_tests.mpy \
  --definition runtime-kompiled \
  --output none

kompile verification.k \
  --backend haskell \
  --main-module ISCube-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled \
  -I .

kprove spec.k \
  --definition verification-kompiled \
  --spec-module ISCube-SPEC \
  --output pretty \
  --warnings none
