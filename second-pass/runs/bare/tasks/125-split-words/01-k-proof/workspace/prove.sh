#!/usr/bin/env bash
set -euo pipefail

# Regenerate the constructor program from the submitted Python source.
python3 py2mpy.py solution.py > solution.mpy

# Build the hand-written semantics with the symbolic Haskell backend.
kompile verification.k \
  --backend haskell \
  --main-module MPY-VERIFICATION \
  --syntax-module MPY-SYNTAX

# Exercise all three contract branches and two precedence/edge cases using the
# actual translated program as $PGM.
krun solution.mpy -cINPUT='"Hello world!"'
krun solution.mpy -cINPUT='"Hello,world!"'
krun solution.mpy -cINPUT='"abcdef"'
krun solution.mpy -cINPUT='"a,b c"'
krun solution.mpy -cINPUT='"a,,b,"'

# Prove the total symbolic contract and every concrete claim in spec.k.
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPLIT-WORDS-SPEC
