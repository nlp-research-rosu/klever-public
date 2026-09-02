#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy
python3 -m py_compile solution.py

kompile semantic.k \
  --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --backend llvm \
  --output-definition semantic-kompiled

krun solution.mpy -d semantic-kompiled \
  -cINPUT='cons(5,cons(8,cons(7,cons(1,nil))))'
krun solution.mpy -d semantic-kompiled \
  -cINPUT='cons(3,cons(3,cons(3,cons(3,cons(3,nil)))))'
krun solution.mpy -d semantic-kompiled \
  -cINPUT='cons(30,cons(13,cons(24,cons(321,nil))))'
krun solution.mpy -d semantic-kompiled \
  -cINPUT='cons(-5,cons(2,cons(-3,nil)))'

kompile verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --backend haskell \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --smt-timeout 1000
