#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy

kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

krun solution.mpy --definition verification-kompiled -cTEXT='""'
krun solution.mpy --definition verification-kompiled -cTEXT='"Hello world"'
krun solution.mpy --definition verification-kompiled \
  -cTEXT='"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"'

kprove spec.k --definition verification-kompiled
