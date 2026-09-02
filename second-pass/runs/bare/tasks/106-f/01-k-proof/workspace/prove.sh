#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy

kompile semantic.k \
  --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --backend llvm

krun solution.mpy -cINPUT=0 --definition semantic-kompiled
krun solution.mpy -cINPUT=5 --definition semantic-kompiled
krun solution.mpy -cINPUT=8 --definition semantic-kompiled

kompile verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --backend haskell

# The proof shorthand expands to exactly the AST translated from solution.py.
diff \
  <(kast solution.mpy --definition verification-kompiled \
      --module VERIFICATION --sort Program --expand-macros --output kore) \
  <(kast --expression solution --definition verification-kompiled \
      --module VERIFICATION --sort Program --expand-macros --output kore)

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --output pretty
