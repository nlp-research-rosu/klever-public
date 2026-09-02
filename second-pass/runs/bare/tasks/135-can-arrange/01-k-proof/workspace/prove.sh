#!/usr/bin/env bash
set -euo pipefail

# Recreate the constructor program from the immutable translator input.
python3 py2mpy.py solution.py > solution.mpy
python3 -m py_compile solution.py

# Build the executable semantics and exercise the actual generated .mpy term.
kompile semantic.k \
  --backend llvm \
  --main-module MPY \
  --syntax-module MPY-SYNTAX \
  -o concrete-kompiled

krun solution.mpy \
  -cARGS='arrayVal(seq(1,2,4,3,5),0,5)' \
  --definition concrete-kompiled \
  | grep -F 'value ( intVal ( 3 ) )'

krun solution.mpy \
  -cARGS='arrayVal(seq(1,2,3),0,3)' \
  --definition concrete-kompiled \
  | grep -F 'value ( intVal ( -1 ) )'

krun solution.mpy \
  -cARGS='arrayVal(seq(5,4,3,2,1),0,5)' \
  --definition concrete-kompiled \
  | grep -F 'value ( intVal ( 4 ) )'

krun solution.mpy \
  -cARGS='arrayVal(seq(),0,0)' \
  --definition concrete-kompiled \
  | grep -F 'value ( intVal ( -1 ) )'

# Include the contract functions and exact generated function tree in the
# Haskell definition, then prove every claim in spec.k.
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION \
  -o proof-kompiled

kprove spec.k \
  --definition proof-kompiled \
  --spec-module SPEC \
  | tee kprove.log

grep -qx '#Top' kprove.log
