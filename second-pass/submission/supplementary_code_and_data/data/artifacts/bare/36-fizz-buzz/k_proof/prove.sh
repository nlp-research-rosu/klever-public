#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

python3 py2mpy.py solution.py > solution.mpy

kompile verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --backend haskell

# The three examples from prompt.py.
krun solution.mpy -cN=50 --definition verification-kompiled
krun solution.mpy -cN=78 --definition verification-kompiled
krun solution.mpy -cN=79 --definition verification-kompiled

# This proves every claim in spec.k.  Success prints #Top and exits zero.
kprove spec.k --definition verification-kompiled
