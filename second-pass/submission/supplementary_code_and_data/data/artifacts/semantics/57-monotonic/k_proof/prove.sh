#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

{
  sed -n '1,200p' solution.py
  printf '%s\n' \
    'assert monotonic([1, 2, 4, 20])' \
    'assert not monotonic([1, 20, 4, 10])' \
    'assert monotonic([4, 1, 0, -10])' \
    'assert monotonic([])' \
    'assert monotonic([3])' \
    'assert monotonic([1, 1, 2, 2])' \
    'assert monotonic([2, 2, 1, 1])'
} | python3 py2mpy.py /dev/stdin \
  | krun /dev/stdin -d runtime-kompiled

kompile verification.k \
  --backend haskell \
  --main-module MONOTONIC-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module MONOTONIC-SPEC
