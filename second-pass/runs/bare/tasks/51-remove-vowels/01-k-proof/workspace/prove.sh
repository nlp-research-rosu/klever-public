#!/usr/bin/env bash
set -euo pipefail

# Regenerate the constructor term from the submitted implementation.
python3 py2mpy.py solution.py > solution.mpy

# Compile the semantics together with its verification definitions.
kompile verification.k \
  --syntax-module MPY-SYNTAX \
  --main-module VERIFICATION \
  --backend haskell

# Exercise every example from prompt.py through the K semantics.
krun solution.mpy -cINPUT='""' --definition verification-kompiled
krun solution.mpy -cINPUT='"abcdef\nghijklm"' --definition verification-kompiled
krun solution.mpy -cINPUT='"abcdef"' --definition verification-kompiled
krun solution.mpy -cINPUT='"aaaaa"' --definition verification-kompiled
krun solution.mpy -cINPUT='"aaBAA"' --definition verification-kompiled
krun solution.mpy -cINPUT='"zbcd"' --definition verification-kompiled

# Prove the universally quantified refinement claim in spec.k.
kprove spec.k --definition verification-kompiled --spec-module SPEC
