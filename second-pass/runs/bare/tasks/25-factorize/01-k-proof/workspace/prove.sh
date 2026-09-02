#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy

kompile semantic.k \
  --backend haskell \
  --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX

krun solution.mpy -cINPUT=8 --definition semantic-kompiled
krun solution.mpy -cINPUT=25 --definition semantic-kompiled
krun solution.mpy -cINPUT=70 --definition semantic-kompiled

kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC

if kprove mutation-spec.k \
     --definition verification-kompiled \
     --spec-module MUTATION-SPEC; then
  echo "error: the deliberately false mutation claim unexpectedly proved" >&2
  exit 1
else
  echo "expected: the deliberately false mutation claim was rejected"
fi
