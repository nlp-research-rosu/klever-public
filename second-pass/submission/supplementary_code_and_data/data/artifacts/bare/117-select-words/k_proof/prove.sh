#!/usr/bin/env bash
set -euo pipefail

# Reproduce the fixed front-end output.
python3 py2mpy.py solution.py > solution.mpy

# Compile and exercise the executable semantics on every prompt example and
# the explicitly required empty-input case.
kompile semantic.k \
  --backend haskell \
  --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX

krun solution.mpy --definition semantic-kompiled \
  -cS='"Mary had a little lamb"' -cN=4
krun solution.mpy --definition semantic-kompiled \
  -cS='"Mary had a little lamb"' -cN=3
krun solution.mpy --definition semantic-kompiled \
  -cS='"simple white space"' -cN=2
krun solution.mpy --definition semantic-kompiled \
  -cS='"Hello world"' -cN=4
krun solution.mpy --definition semantic-kompiled \
  -cS='"Uncle sam"' -cN=3
krun solution.mpy --definition semantic-kompiled \
  -cS='""' -cN=0

# Add the independent contract symbol to the compiled definition, then prove
# every claim in spec.k.  Success is exactly exit status 0 with "#Top".
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
