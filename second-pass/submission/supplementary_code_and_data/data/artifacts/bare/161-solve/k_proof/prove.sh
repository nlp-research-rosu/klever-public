#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

# Recreate the checked constructor program from the immutable translator input.
python3 py2mpy.py solution.py > solution.mpy

# Compile the executable semantics and exercise all prompt examples, plus the
# empty-string boundary case.
kompile semantic.k \
  --backend haskell \
  --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX
krun solution.mpy --definition semantic-kompiled -cINPUT='pstr("1234")'
krun solution.mpy --definition semantic-kompiled -cINPUT='pstr("ab")'
krun solution.mpy --definition semantic-kompiled -cINPUT='pstr("#a@C")'
krun solution.mpy --definition semantic-kompiled -cINPUT='pstr("")'

# Compile the contract layer and prove every claim in spec.k.
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX
kprove spec.k --definition verification-kompiled --spec-module SPEC
