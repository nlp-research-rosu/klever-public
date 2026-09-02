#!/bin/sh
set -eu

cd "$(dirname "$0")"

python3 py2mpy.py solution.py > solution.mpy

kompile semantic.k \
  --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --warnings none

krun solution.mpy -cN=3 --definition semantic-kompiled --output pretty
krun solution.mpy -cN=12 --definition semantic-kompiled --output pretty
krun solution.mpy -cN=1000 --definition semantic-kompiled --output pretty

kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --warnings none

kprove spec.k --definition verification-kompiled --warnings none
