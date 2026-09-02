#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete_calls.py > concrete_calls.mpy
python3 compose_mpy.py solution.mpy concrete_calls.mpy > concrete_tests.mpy
python3 py2mpy.py expansion_call.py > expansion_call.mpy
python3 compose_mpy.py solution.mpy expansion_call.mpy > expansion_test.mpy

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun concrete_tests.mpy \
  --definition runtime-kompiled \
  --output none

krun expansion_test.mpy \
  --definition runtime-kompiled \
  --output none

kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove \
  --definition verification-kompiled \
  --spec-module SPEC \
  spec.k
