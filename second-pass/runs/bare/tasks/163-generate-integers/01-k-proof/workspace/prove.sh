#!/usr/bin/env bash
set -euo pipefail

cd -- "$(dirname -- "$0")"

python3 py2mpy.py solution.py > solution.mpy

kompile semantic.k \
  --backend llvm \
  --main-module MPY \
  --syntax-module MPY-SYNTAX

krun solution.mpy --definition semantic-kompiled -cA=2 -cB=8
krun solution.mpy --definition semantic-kompiled -cA=8 -cB=2
krun solution.mpy --definition semantic-kompiled -cA=10 -cB=14
krun solution.mpy --definition semantic-kompiled -cA=3 -cB=7

kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
