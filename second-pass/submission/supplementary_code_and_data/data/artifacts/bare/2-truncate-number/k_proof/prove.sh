#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

# Recreate the checked constructor tree with the fixed translator.
python3 py2mpy.py solution.py > solution.mpy

# One Haskell-backend definition supports concrete execution and proof.
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module SEMANTIC-SYNTAX

# Exercise the exact translated program on the prompt example, 3.5.
krun solution.mpy \
  --definition verification-kompiled \
  -cIPART=3 -cFRAC=5 -cSCALE=10

# Prove every claim in spec.k.  Success prints #Top and exits zero.
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC

# Sanity check: an intentionally wrong result must not be provable.
if kprove mutation-spec.k \
    --definition verification-kompiled \
    --spec-module MUTATION-SPEC; then
  echo "ERROR: the deliberately false mutation claim unexpectedly proved" >&2
  exit 1
else
  echo "Expected failure: mutation claim was rejected"
fi
