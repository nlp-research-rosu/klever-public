#!/usr/bin/env bash
set -euo pipefail

cd -- "$(dirname -- "$0")"

# Regenerate the submitted constructor tree with the fixed translator.
python3 py2mpy.py solution.py > solution.mpy

# The verification module imports semantic.k and adds only contract vocabulary.
kompile verification.k \
  --backend haskell \
  --main-module HUMAN-EVAL-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled-haskell

# Parse/load the generated source term, then execute negative and positive cases.
krun solution.mpy --definition verification-kompiled-haskell
krun run-unbalanced.mpy --definition verification-kompiled-haskell
krun run-balanced.mpy --definition verification-kompiled-haskell

# Prove the universal contract and every concrete example claim in spec.k.
kprove \
  --definition verification-kompiled-haskell \
  --spec-module WILL-IT-FLY-SPEC \
  spec.k
