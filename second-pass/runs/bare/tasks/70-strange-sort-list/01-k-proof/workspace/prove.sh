#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy
python3 -m py_compile solution.py

kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX

# Exercise the generated program under the semantics on all prompt examples.
krun solution.mpy --definition verification-kompiled \
  -cENTRY='"strange_sort_list"' \
  -cINPUT='cons(1, cons(2, cons(3, cons(4, nil))))'
krun solution.mpy --definition verification-kompiled \
  -cENTRY='"strange_sort_list"' \
  -cINPUT='cons(5, cons(5, cons(5, cons(5, nil))))'
krun solution.mpy --definition verification-kompiled \
  -cENTRY='"strange_sort_list"' \
  -cINPUT='nil'

# Exercise an unsorted odd-length input containing a negative and a duplicate.
krun solution.mpy --definition verification-kompiled \
  -cENTRY='"strange_sort_list"' \
  -cINPUT='cons(3, cons(-1, cons(2, cons(3, cons(0, nil)))))'

# Positive target proof: all 39 claims must close in this one invocation.
kprove spec.k --definition verification-kompiled --spec-module SPEC
