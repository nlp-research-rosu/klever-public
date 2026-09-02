#!/usr/bin/env bash
set -euo pipefail

cd -- "$(dirname -- "$0")"

# Regenerate the constructor program with the fixed translator.
python3 py2mpy.py solution.py > solution.mpy

# VERIFICATION imports SEMANTIC, so this compiles both the interpreter and the
# concrete observer used by the specifications.
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX

# Exercise the translated artifact itself on every example from prompt.py.
krun solution.mpy --definition verification-kompiled -cN=1 -cM=5 \
  | grep -F 'result ( binVal ( 3 ) )'
krun solution.mpy --definition verification-kompiled -cN=7 -cM=5 \
  | grep -F 'result ( intVal ( -1 ) )'
krun solution.mpy --definition verification-kompiled -cN=10 -cM=20 \
  | grep -F 'result ( binVal ( 15 ) )'
krun solution.mpy --definition verification-kompiled -cN=20 -cM=33 \
  | grep -F 'result ( binVal ( 26 ) )'

# Prove all universal partition claims, prompt examples, and rendering claims.
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --output pretty
