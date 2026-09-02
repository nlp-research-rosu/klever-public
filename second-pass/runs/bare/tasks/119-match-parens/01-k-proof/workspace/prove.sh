#!/usr/bin/env bash
set -euo pipefail

# Regenerate the submitted constructor program from the submitted Python.
python3 py2mpy.py solution.py > solution.mpy

# Build and exercise the operational semantics on both prompt examples.
kompile semantic.k \
  --backend haskell \
  --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --output-definition semantic-kompiled

krun solution.mpy \
  --definition semantic-kompiled \
  -cINPUT='ListExpr(Str("()("), Str(")"))' \
  | grep -F 'strVal ( yesString )'

krun solution.mpy \
  --definition semantic-kompiled \
  -cINPUT='ListExpr(Str(")"), Str(")"))' \
  | grep -F 'strVal ( noString )'

# Build the verification extension and prove every claim in spec.k.
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-VERIFICATION \
  --output-definition verification-kompiled

kprove spec.k --definition verification-kompiled
