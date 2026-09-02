#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy
python3 -m py_compile solution.py

kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX

krun solution.mpy \
  -cINPUT='pyList(ListItem(1) ListItem(2) ListItem(3))' \
  --definition verification-kompiled

krun solution.mpy \
  -cINPUT='pyList(ListItem(5) ListItem(6) ListItem(3) ListItem(4))' \
  --definition verification-kompiled

krun solution.mpy \
  -cINPUT='pyList(ListItem(-1) ListItem(7) ListItem(-3) ListItem(6) ListItem(0))' \
  --definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  -w none
