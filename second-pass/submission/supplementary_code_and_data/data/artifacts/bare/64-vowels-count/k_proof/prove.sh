#!/usr/bin/env bash
set -euo pipefail

# Regenerate and check the fixed translator's output.
python3 py2mpy.py solution.py > .solution.generated.mpy
cmp solution.mpy .solution.generated.mpy
rm .solution.generated.mpy

# VERIFICATION imports SEMANTIC, adding only the independent #vowels oracle.
kompile verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --backend haskell

# Execute the prompt examples and edge cases through the K semantics.
krun solution.mpy --definition verification-kompiled -cINPUT='"abcde"' --output pretty
krun solution.mpy --definition verification-kompiled -cINPUT='"ACEDY"' --output pretty
krun solution.mpy --definition verification-kompiled -cINPUT='""' --output pretty
krun solution.mpy --definition verification-kompiled -cINPUT='"rhythm"' --output pretty
krun solution.mpy --definition verification-kompiled -cINPUT='"y"' --output pretty

# Prove every claim in spec.k; successful output is #Top.
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --output pretty
