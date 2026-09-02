#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy

# The Haskell backend supports both concrete execution and reachability proof.
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module TINY-PYTHON-SYNTAX

# Execute the actual generated constructor program on the documented example.
krun solution.mpy \
  --definition verification-kompiled \
  -cARGS='Args(5, 3)'

# Prove every reachability claim in spec.k.
kprove spec.k --definition verification-kompiled
