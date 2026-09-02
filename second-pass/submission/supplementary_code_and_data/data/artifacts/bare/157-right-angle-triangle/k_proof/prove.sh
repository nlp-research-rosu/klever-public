#!/usr/bin/env bash
set -euo pipefail

cd -- "$(dirname -- "$0")"

python3 py2mpy.py solution.py > solution.mpy
python3 -m py_compile solution.py

kompile semantic.k \
  --backend haskell \
  --main-module MPY \
  --syntax-module MPY-SYNTAX

krun run-3-4-5.mpy \
  --definition semantic-kompiled \
  | grep -F 'result ( true )'

kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
