#!/usr/bin/env bash
set -euo pipefail

# Recreate the K input from the unmodified translator.
python3 py2mpy.py solution.py > solution.mpy

# Build the semantics for both concrete execution and symbolic proof.
kompile semantic.k \
  --backend haskell \
  --main-module MPY \
  --syntax-module MPY-SYNTAX

# Exercise all remainder classes and a multi-block input.  These arguments
# are outputs of encode_cyclic for "", "a", "ab", "abc", and "abcdefgh".
krun solution.mpy -cS='""'
krun solution.mpy -cS='"a"'
krun solution.mpy -cS='"ab"'
krun solution.mpy -cS='"bca"'
krun solution.mpy -cS='"bcaefdgh"'

# Prove both claims in spec.k (the loop invariant and end-to-end theorem).
kprove spec.k --definition semantic-kompiled --spec-module SPEC
