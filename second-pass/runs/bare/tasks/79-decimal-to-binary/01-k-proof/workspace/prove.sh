#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy
kompile verification.k --backend haskell --syntax-module SEMANTIC-SYNTAX \
  --output-definition .kbuild
krun solution.mpy --definition .kbuild -cARG=0
krun solution.mpy --definition .kbuild -cARG=-5
krun solution.mpy --definition .kbuild -cARG=15
krun solution.mpy --definition .kbuild -cARG=32
kprove spec.k --definition .kbuild
