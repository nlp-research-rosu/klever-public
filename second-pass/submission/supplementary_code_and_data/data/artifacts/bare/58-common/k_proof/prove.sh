#!/usr/bin/env bash
set -euo pipefail

cd -- "$(dirname -- "$0")"

# Recreate the checked constructor program from the submitted Python source.
python3 py2mpy.py solution.py > solution.mpy

# The verification definition imports the executable semantics and adds only
# the mathematical commonSpec operation.
kompile verification.k \
  --main-module VERIFICATION \
  --syntax-module SEMANTIC-SYNTAX \
  --backend haskell

# Exercise both prompt examples plus duplicate/negative and empty-list cases.
krun solution.mpy --definition verification-kompiled \
  -cL1='list(1,4,3,34,653,2,5)' \
  -cL2='list(5,7,1,5,9,653,121)'
krun solution.mpy --definition verification-kompiled \
  -cL1='list(5,3,2,8)' \
  -cL2='list(3,2)'
krun solution.mpy --definition verification-kompiled \
  -cL1='list(3,3,-1,2)' \
  -cL2='list(3,-1,-1)'
krun solution.mpy --definition verification-kompiled \
  -cL1='list()' \
  -cL2='list(1,1)'

# Positive target proof: this must print #Top and exit zero.
kprove spec.k --definition verification-kompiled --spec-module SPEC

# Expected-failure mutation probe.  If this proves, the validation is unsound.
if kprove mutation-spec.k \
    --definition verification-kompiled \
    --spec-module MUTATION-SPEC; then
  echo 'ERROR: the deliberately incorrect mutation unexpectedly proved' >&2
  exit 1
else
  echo 'Expected failure: the l1/l1 intersection mutation was rejected.'
fi
