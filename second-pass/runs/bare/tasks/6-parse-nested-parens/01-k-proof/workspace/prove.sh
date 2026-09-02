#!/usr/bin/env bash
set -euo pipefail

cd -- "$(dirname -- "$0")"

# Translate the submitted Python source without modifying the fixed front end.
python3 py2mpy.py solution.py > solution.mpy

# Build the executable semantics and exercise the actual translated program.
kompile semantic.k \
  --main-module MPY-SEMANTICS \
  --syntax-module MPY-SYNTAX \
  --backend llvm
krun solution.mpy \
  --definition semantic-kompiled \
  -cINPUT='"(()()) ((())) () ((())()())"'

# Build the proof definition and close every positive claim in spec.k.
kompile verification.k \
  --main-module MPY-VERIFICATION \
  --syntax-module MPY-VERIFICATION \
  --backend haskell
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC

# A wrong expected answer must not prove.
if kprove mutation-spec.k \
     --definition verification-kompiled \
     --spec-module MUTATION-SPEC; then
  echo "ERROR: the deliberately false mutation claim unexpectedly proved" >&2
  exit 1
else
  echo "Expected failure: mutation claim was rejected"
fi
