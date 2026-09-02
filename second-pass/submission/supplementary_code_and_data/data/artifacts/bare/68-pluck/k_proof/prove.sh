#!/usr/bin/env bash
set -euo pipefail

# Recreate the translated program from the fixed translator.
python3 py2mpy.py solution.py > solution.mpy

# The LLVM definition is used only for ordinary concrete execution.
kompile semantic.k \
  --backend llvm \
  --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX

# Exercise every example from prompt.py with the operational semantics.
krun solution.mpy --definition semantic-kompiled -cARGS='VList(4, 2, 3)'
krun solution.mpy --definition semantic-kompiled -cARGS='VList(1, 2, 3)'
krun solution.mpy --definition semantic-kompiled -cARGS='VList()'
krun solution.mpy --definition semantic-kompiled -cARGS='VList(5, 0, 3, 0, 4, 2)'
krun solution.mpy --definition semantic-kompiled -cARGS='VList(7, 5, 9)'
krun solution.mpy --definition semantic-kompiled -cARGS='VList(2, 2)'

# The Haskell backend proves the universal claim in spec.k.  The final command
# prints #Top and exits 0.
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX
kprove spec.k --definition verification-kompiled
