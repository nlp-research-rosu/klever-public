#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy
kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module VERIFICATION

krun solution.mpy --definition verification-kompiled
krun example1.mpy --definition verification-kompiled
krun example2.mpy --definition verification-kompiled

kprove spec.k --definition verification-kompiled
