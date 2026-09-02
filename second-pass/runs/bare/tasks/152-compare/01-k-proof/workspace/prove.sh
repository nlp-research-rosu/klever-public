#!/usr/bin/env bash
set -euo pipefail

# Recreate the fixed translator output from the submitted implementation.
python3 py2mpy.py solution.py > solution.mpy
printf '%s  %s\n' \
  '8b1459d8f7e47fe17ad740613f5b14392282cdd23d81b304779d1994f6c83e5b' \
  'solution.mpy' | sha256sum --check --strict -

# Check the ordinary Python behavior on both examples from prompt.py.
python3 - <<'PY'
from solution import compare

assert compare([1, 2, 3, 4, 5, 1], [1, 2, 3, 4, 2, -2]) == [0, 0, 0, 0, 3, 3]
assert compare([0, 5, 0, 0, 0, 4], [4, 1, 1, 0, 0, -2]) == [4, 4, 1, 0, 0, 6]
print("Python prompt examples passed")
PY

# Compile the executable semantics and exercise both prompt examples in K.
kompile semantic.k --backend llvm --main-module SEMANTIC --syntax-module MPY-SYNTAX
krun solution.mpy --definition semantic-kompiled \
  -cGAME='VList(VCons(VInt(1), VCons(VInt(2), VCons(VInt(3), VCons(VInt(4), VCons(VInt(5), VCons(VInt(1), VNil)))))))' \
  -cGUESS='VList(VCons(VInt(1), VCons(VInt(2), VCons(VInt(3), VCons(VInt(4), VCons(VInt(2), VCons(VInt(-2), VNil)))))))'
krun solution.mpy --definition semantic-kompiled \
  -cGAME='VList(VCons(VInt(0), VCons(VInt(5), VCons(VInt(0), VCons(VInt(0), VCons(VInt(0), VCons(VInt(4), VNil)))))))' \
  -cGUESS='VList(VCons(VInt(4), VCons(VInt(1), VCons(VInt(1), VCons(VInt(0), VCons(VInt(0), VCons(VInt(-2), VNil)))))))'

# Compile the proof definition and prove every claim in spec.k.
kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX
kprove spec.k --definition verification-kompiled --spec-module SPEC
