#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy

kompile semantic.k \
  --backend haskell \
  --syntax-module MPY-SYNTAX \
  --main-module SEMANTIC

krun solution.mpy --definition semantic-kompiled \
  -cARGS='listVal(intVal(0), intVal(3), intVal(2), intVal(1), intVal(3), intVal(5), intVal(7), intVal(4), intVal(5), intVal(5), intVal(5), intVal(2), intVal(181), intVal(32), intVal(4), intVal(32), intVal(3), intVal(2), intVal(32), intVal(324), intVal(4), intVal(3))' \
  | grep -q 'result ( intVal ( 10 ) )'

krun solution.mpy --definition semantic-kompiled \
  -cARGS='listVal(intVal(1), intVal(0), intVal(1), intVal(8), intVal(2), intVal(4597), intVal(2), intVal(1), intVal(3), intVal(40), intVal(1), intVal(2), intVal(1), intVal(2), intVal(4), intVal(2), intVal(5), intVal(1))' \
  | grep -q 'result ( intVal ( 25 ) )'

krun solution.mpy --definition semantic-kompiled \
  -cARGS='listVal(intVal(1), intVal(3), intVal(1), intVal(32), intVal(5107), intVal(34), intVal(83278), intVal(109), intVal(163), intVal(23), intVal(2323), intVal(32), intVal(30), intVal(1), intVal(9), intVal(3))' \
  | grep -q 'result ( intVal ( 13 ) )'

krun solution.mpy --definition semantic-kompiled \
  -cARGS='listVal(intVal(0), intVal(724), intVal(32), intVal(71), intVal(99), intVal(32), intVal(6), intVal(0), intVal(5), intVal(91), intVal(83), intVal(0), intVal(5), intVal(6))' \
  | grep -q 'result ( intVal ( 11 ) )'

krun solution.mpy --definition semantic-kompiled \
  -cARGS='listVal(intVal(0), intVal(81), intVal(12), intVal(3), intVal(1), intVal(21))' \
  | grep -q 'result ( intVal ( 3 ) )'

krun solution.mpy --definition semantic-kompiled \
  -cARGS='listVal(intVal(0), intVal(8), intVal(1), intVal(2), intVal(1), intVal(7))' \
  | grep -q 'result ( intVal ( 7 ) )'

kompile verification.k \
  --backend haskell \
  --syntax-module MPY-SYNTAX \
  --main-module VERIFICATION

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
