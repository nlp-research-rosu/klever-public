#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy

mkdir -p build
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module SEMANTIC-SYNTAX \
  --output-definition build/verification-kompiled

krun solution.mpy \
  -cARG='listVal(cons(1, cons(2, cons(4, cons(20, nil)))))' \
  --definition build/verification-kompiled
krun solution.mpy \
  -cARG='listVal(cons(1, cons(20, cons(4, cons(10, nil)))))' \
  --definition build/verification-kompiled
krun solution.mpy \
  -cARG='listVal(cons(4, cons(1, cons(0, cons(-10, nil)))))' \
  --definition build/verification-kompiled

kprove spec.k \
  --definition build/verification-kompiled \
  --spec-module SPEC
