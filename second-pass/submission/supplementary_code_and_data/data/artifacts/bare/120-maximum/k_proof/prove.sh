#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy

kompile verification.k \
  --backend haskell \
  --main-module MAXIMUM-VERIFICATION \
  --syntax-module MAXIMUM-SYNTAX

krun solution.mpy --definition verification-kompiled \
  -cARGS='ListItem(listVal(ListItem(-3) ListItem(-4) ListItem(5))) ListItem(intVal(3))'
krun solution.mpy --definition verification-kompiled \
  -cARGS='ListItem(listVal(ListItem(4) ListItem(-4) ListItem(4))) ListItem(intVal(2))'
krun solution.mpy --definition verification-kompiled \
  -cARGS='ListItem(listVal(ListItem(-3) ListItem(2) ListItem(1) ListItem(2) ListItem(-1) ListItem(-2) ListItem(1))) ListItem(intVal(1))'
krun solution.mpy --definition verification-kompiled \
  -cARGS='ListItem(listVal(ListItem(7) ListItem(-1))) ListItem(intVal(0))'

kprove spec.k \
  --definition verification-kompiled \
  --spec-module MAXIMUM-SPEC
