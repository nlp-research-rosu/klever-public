#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy

kompile semantic.k \
  --backend haskell \
  --main-module MPY-SEMANTICS \
  --syntax-module MPY-SYNTAX

krun solution.mpy \
  --definition semantic-kompiled \
  -cARR='ListItem(111) ListItem(21) ListItem(3) ListItem(4000) ListItem(5) ListItem(6) ListItem(7) ListItem(8) ListItem(9)' \
  -cN=4 \
  | grep -F 'result ( 24 )'

krun solution.mpy \
  --definition semantic-kompiled \
  -cARR='ListItem(-100) ListItem(-99) ListItem(-1) ListItem(0) ListItem(9) ListItem(10) ListItem(99) ListItem(100)' \
  -cN=8 \
  | grep -F 'result ( 18 )'

kompile verification.k \
  --backend haskell \
  --main-module MPY-VERIFICATION \
  --syntax-module MPY-SYNTAX

# The proof's solutionProgram macro must expand to the exact translated AST.
diff -u \
  <(kast solution.mpy \
      --definition verification-kompiled \
      --module MPY-VERIFICATION \
      --sort Program \
      --expand-macros \
      --output kast) \
  <(kast \
      --expression solutionProgram \
      --definition verification-kompiled \
      --module MPY-VERIFICATION \
      --sort Program \
      --expand-macros \
      --output kast)

kprove spec.k \
  --definition verification-kompiled \
  --spec-module ADD-ELEMENTS-SPEC
