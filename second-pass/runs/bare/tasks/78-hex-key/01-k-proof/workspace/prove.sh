#!/usr/bin/env bash
set -euo pipefail

# Regenerate the constructor program from the unmodified translator.
python3 py2mpy.py solution.py > solution.mpy

# Build the executable semantics and exercise the empty edge case and every
# example from prompt.py.
kompile semantic.k --backend haskell --main-module MPY --syntax-module MPY-SYNTAX
krun solution.mpy -d semantic-kompiled -cINPUT='""' --output pretty
krun solution.mpy -d semantic-kompiled -cINPUT='"AB"' --output pretty
krun solution.mpy -d semantic-kompiled -cINPUT='"1077E"' --output pretty
krun solution.mpy -d semantic-kompiled -cINPUT='"ABED1A33"' --output pretty
krun solution.mpy -d semantic-kompiled -cINPUT='"123456789ABCDEF0"' --output pretty
krun solution.mpy -d semantic-kompiled -cINPUT='"2020"' --output pretty

# Compile the mathematical contract helper into the definition, then prove
# every claim in spec.k (one universal all-String functional-correctness claim).
kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX
kprove spec.k --definition verification-kompiled --spec-module HEX-KEY-SPEC
