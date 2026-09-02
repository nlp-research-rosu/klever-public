#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

python3 py2mpy.py solution.py > solution.mpy

kompile semantic.k \
  --backend haskell \
  --main-module MPY \
  --syntax-module MPY-SYNTAX

# Exercise all examples from prompt.py through the semantics.
krun solution.mpy --definition semantic-kompiled -cN=4
krun solution.mpy --definition semantic-kompiled -cN=6
krun solution.mpy --definition semantic-kompiled -cN=8

# Compile the verification abstraction into the proof definition, then prove
# every claim in spec.k.  Success prints #Top and exits zero.
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
