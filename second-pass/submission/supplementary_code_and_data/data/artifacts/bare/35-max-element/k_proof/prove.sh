#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy

kompile semantic.k \
  --backend haskell \
  --main-module MPY-SEMANTICS \
  --syntax-module MPY-SYNTAX \
  --output-definition semantic-kompiled

krun solution.mpy \
  --definition semantic-kompiled \
  -cARGS='[1, 2, 3]'

krun solution.mpy \
  --definition semantic-kompiled \
  -cARGS='[5, 3, -5, 2, -3, 3, 9, 0, 123, 1, -10]'

kompile verification.k \
  --backend haskell \
  --main-module MPY-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
