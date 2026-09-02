#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

# Recreate the fixed translator's exact program term.
python3 py2mpy.py solution.py > solution.mpy

# Exercise the actual translated program with the executable semantics.
kompile semantic.k \
  --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --backend llvm \
  -o semantic-llvm-kompiled
krun solution.mpy -d semantic-llvm-kompiled -cA=3 -cB=5 \
  | grep -F "result ( 1 )"
krun solution.mpy -d semantic-llvm-kompiled -cA=25 -cB=15 \
  | grep -F "result ( 5 )"
krun solution.mpy -d semantic-llvm-kompiled -cA=-25 -cB=15 \
  | grep -F "result ( 5 )"
krun solution.mpy -d semantic-llvm-kompiled -cA=0 -cB=0 \
  | grep -F "result ( 0 )"

# First prove the symbolic Euclidean-loop theorem against semantic.k alone.
kompile loop-verification.k \
  --main-module LOOP-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --backend haskell \
  -o loop-kompiled
kprove loop-spec.k --definition loop-kompiled

# Compile that discharged theorem as the verification lemma, then prove the
# universal whole-program claim in spec.k.
kompile verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --backend haskell \
  -o verification-kompiled
kprove spec.k --definition verification-kompiled
