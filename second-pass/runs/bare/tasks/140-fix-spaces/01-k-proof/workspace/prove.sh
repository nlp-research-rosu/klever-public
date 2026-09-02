#!/usr/bin/env bash
set -euo pipefail

# Regenerate the exact constructor program from the submitted Python source.
python3 py2mpy.py solution.py > solution.mpy

# Compile the executable semantics and exercise every example in prompt.py.
kompile --backend haskell semantic.k \
  --main-module MPY-SEMANTIC --syntax-module MPY-SYNTAX
krun solution.mpy -d semantic-kompiled -cINPUT='"Example"'
krun solution.mpy -d semantic-kompiled -cINPUT='"Example 1"'
krun solution.mpy -d semantic-kompiled -cINPUT='" Example 2"'
krun solution.mpy -d semantic-kompiled -cINPUT='" Example   3"'

# Compile the exact translated program data plus the independent reference
# relation, then prove all claims in spec.k.
kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX
kprove spec.k --definition verification-kompiled --spec-module SPEC
