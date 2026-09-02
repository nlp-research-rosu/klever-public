#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy

kompile semantic.k \
  --backend llvm \
  --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX \
  -o semantic-kompiled

# The four examples from prompt.py.
krun solution.mpy -d semantic-kompiled \
  -cINPUT='cons(1,cons(2,cons(3,cons(4,cons(5,nil)))))'
krun solution.mpy -d semantic-kompiled \
  -cINPUT='cons(5,cons(1,cons(4,cons(3,cons(2,nil)))))'
krun solution.mpy -d semantic-kompiled -cINPUT='nil'
krun solution.mpy -d semantic-kompiled -cINPUT='cons(1,cons(1,nil))'

kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  -o verification-kompiled

# Universal positive target: this must print #Top and exit zero.
kprove spec.k \
  -d verification-kompiled \
  --spec-module SPEC \
  --claims next-smallest-correct \
  --output pretty
