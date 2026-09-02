#!/usr/bin/env bash
set -euo pipefail

# Translate the submitted Python source with the fixed front end.
python3 py2mpy.py solution.py > solution.mpy

# Build the semantics with the proof-capable backend.
kompile semantic.k \
  --main-module SEMANTIC \
  --syntax-module SEMANTIC-SYNTAX \
  --backend haskell

# Exercise both prompt examples and a delimiter edge case concretely.
krun solution.mpy -cINPUT='"Hi, my name is John"'
krun solution.mpy -cINPUT='"One, two, three, four, five, six"'
krun solution.mpy -cINPUT='"  alpha,,beta   gamma, "'

# Prove every claim in spec.k, including the universal correctness claim.
kprove \
  --definition semantic-kompiled \
  --spec-module SPEC \
  spec.k
