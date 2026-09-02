#!/usr/bin/env bash
set -eu

python3 py2mpy.py solution.py > solution.mpy

kompile semantic.k \
  --backend haskell \
  --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX

krun solution.mpy \
  -cINPUT='ListItem(1) ListItem(2) ListItem(3) ListItem(5) ListItem(4) ListItem(7) ListItem(9) ListItem(6)' \
  --definition semantic-kompiled
krun solution.mpy \
  -cINPUT='ListItem(1) ListItem(2) ListItem(3) ListItem(4) ListItem(3) ListItem(2) ListItem(2)' \
  --definition semantic-kompiled
krun solution.mpy \
  -cINPUT='ListItem(1) ListItem(2) ListItem(3) ListItem(2) ListItem(1)' \
  --definition semantic-kompiled

kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
