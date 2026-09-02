#!/usr/bin/env bash
set -euo pipefail

cd -- "$(dirname -- "$0")"

# Recreate the required pure AST translation and check the Python behavior.
python3 py2mpy.py solution.py > solution.mpy
python3 -m py_compile solution.py
python3 - <<'PY'
from solution import count_nums

assert count_nums([]) == 0
assert count_nums([-1, 11, -11]) == 1
assert count_nums([1, 1, 2]) == 3
assert count_nums([-123, -100, -99, 0, 10]) == 2
PY

# Build the executable semantics and exercise the translated constructor tree.
kompile semantic.k \
  --main-module MPY-SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --backend llvm \
  -o semantic-kompiled

krun solution.mpy -d semantic-kompiled -cARG='list()' \
  | grep -F 'IntV ( 0 ) ~> .K'
krun solution.mpy -d semantic-kompiled -cARG='list(-1, 11, -11)' \
  | grep -F 'IntV ( 1 ) ~> .K'
krun solution.mpy -d semantic-kompiled -cARG='list(1, 1, 2)' \
  | grep -F 'IntV ( 3 ) ~> .K'
krun solution.mpy -d semantic-kompiled \
  -cARG='list(-123, -100, -99, 0, 10)' \
  | grep -F 'IntV ( 2 ) ~> .K'

# Build the symbolic verification definition, then prove every claim in SPEC.
kompile verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --backend haskell \
  -o verification-kompiled

kprove spec.k -d verification-kompiled --spec-module SPEC
