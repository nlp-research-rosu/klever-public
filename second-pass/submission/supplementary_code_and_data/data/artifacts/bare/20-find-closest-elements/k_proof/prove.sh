#!/usr/bin/env bash
set -euo pipefail

# Regenerate the constructor program from the submitted Python source.
python3 py2mpy.py solution.py > solution.mpy

# Parse and execute the generated module itself.
kompile semantic.k \
  --backend llvm \
  --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition semantic-llvm-kompiled
krun solution.mpy \
  --definition semantic-llvm-kompiled \
  --output pretty

# Exercise an actual entry-point invocation through the semantics.
kompile verification.k \
  --backend llvm \
  --main-module MPY-VERIFICATION \
  --syntax-module MPY-VERIFICATION \
  --output-definition verification-llvm-kompiled
krun example.run \
  --definition verification-llvm-kompiled \
  --output pretty

# Prove every reachability claim in spec.k.
kompile verification.k \
  --backend haskell \
  --main-module MPY-VERIFICATION \
  --syntax-module MPY-VERIFICATION \
  --output-definition verification-proof-kompiled
kprove spec.k \
  --definition verification-proof-kompiled \
  --spec-module SPEC
