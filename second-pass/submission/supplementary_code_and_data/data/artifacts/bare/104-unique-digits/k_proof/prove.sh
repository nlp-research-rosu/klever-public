#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

python3 py2mpy.py solution.py > solution.mpy

PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
from solution import unique_digits

assert unique_digits([15, 33, 1422, 1]) == [1, 15, 33]
assert unique_digits([152, 323, 1422, 10]) == []
assert unique_digits([97531, 7, 111, 97531]) == [7, 111, 97531, 97531]
PY

kompile semantic.k \
  --backend haskell \
  --main-module MPY-SEMANTIC \
  --syntax-module MPY-SYNTAX

krun solution.mpy --definition semantic-kompiled \
  -cARGS='pyList(cons(15, cons(33, cons(1422, cons(1, .Ints)))))' \
  | grep -F 'pyList ( cons ( 1 , cons ( 15 , cons ( 33 , .Ints ) ) ) )'
krun solution.mpy --definition semantic-kompiled \
  -cARGS='pyList(cons(152, cons(323, cons(1422, cons(10, .Ints)))))' \
  | grep -F 'pyList ( .Ints )'
krun solution.mpy --definition semantic-kompiled \
  -cARGS='pyList(cons(97531, cons(7, cons(111, cons(97531, .Ints)))))' \
  | grep -F 'pyList ( cons ( 7 , cons ( 111 , cons ( 97531 , cons ( 97531 , .Ints ) ) ) ) )'

kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
