#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

python3 py2mpy.py <(
  sed -n '1,$p' solution.py
  printf '%s\n' \
    'assert fib4(0) == 0' \
    'assert fib4(1) == 0' \
    'assert fib4(2) == 2' \
    'assert fib4(3) == 0' \
    'assert fib4(5) == 4' \
    'assert fib4(6) == 8' \
    'assert fib4(7) == 14' \
    'assert fib4(10) == 104'
) > concrete-tests.mpy

krun concrete-tests.mpy --definition runtime-kompiled

kompile verification.k \
  --backend haskell \
  --main-module FIB4-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module FIB4-SPEC \
  --claims FIB4-SPEC.loop-step \
  --output pretty

kprove spec.k \
  --definition verification-kompiled \
  --spec-module FIB4-SPEC \
  --claims FIB4-SPEC.operational-cases \
  --output pretty
