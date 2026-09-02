#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy

kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX

krun solution.mpy \
  --definition verification-kompiled \
  -cINPUT='""'
krun solution.mpy \
  --definition verification-kompiled \
  -cINPUT='"abc"'

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
