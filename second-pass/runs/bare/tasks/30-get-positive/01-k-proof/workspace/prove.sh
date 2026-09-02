#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy

kompile semantic.k \
  --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --backend haskell

krun solution.mpy \
  -cINPUT='cons(-1, cons(2, cons(-4, cons(5, cons(6, nil)))))'

krun solution.mpy \
  -cINPUT='cons(5, cons(3, cons(-5, cons(2, cons(-3, cons(3, cons(9, cons(0, cons(123, cons(1, cons(-10, nil)))))))))))'

kprove spec.k --definition semantic-kompiled
