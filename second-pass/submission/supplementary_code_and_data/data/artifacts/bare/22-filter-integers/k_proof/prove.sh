#!/usr/bin/env bash
set -euo pipefail

# Recreate the constructor term from the submitted Python implementation.
python3 py2mpy.py solution.py > solution.mpy

# Check the executable Python against the prompt examples and boundary cases.
python3 - <<'PY'
from solution import filter_integers

cases = [
    (["a", 3.14, 5], [5]),
    ([1, 2, 3, "abc", {}, []], [1, 2, 3]),
    ([True, False, 0, -4, 2.0], [True, False, 0, -4]),
    ([], []),
]
for values, expected in cases:
    assert filter_integers(values) == expected
PY

# Compile the executable semantics and check the exact final K results.
kompile semantic.k \
  --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --backend llvm \
  --output-definition semantic-kompiled

krun solution.mpy -d semantic-kompiled \
  -cINPUT='VList(VString("a"), VFloat("3.14"), VInt(5))' \
  | tr -d '[:space:]' \
  | rg --fixed-strings --quiet 'result(VList(VInt(5),.PyVals))'

krun solution.mpy -d semantic-kompiled \
  -cINPUT='VList(VInt(1), VInt(2), VInt(3), VString("abc"), VDict, VList())' \
  | tr -d '[:space:]' \
  | rg --fixed-strings --quiet \
      'result(VList(VInt(1),VInt(2),VInt(3),.PyVals))'

krun solution.mpy -d semantic-kompiled \
  -cINPUT='VList(VBool(true), VBool(false), VInt(0), VInt(-4), VFloat("2.0"))' \
  | tr -d '[:space:]' \
  | rg --fixed-strings --quiet \
      'result(VList(VBool(true),VBool(false),VInt(0),VInt(-4),.PyVals))'

krun solution.mpy -d semantic-kompiled -cINPUT='VList()' \
  | tr -d '[:space:]' \
  | rg --fixed-strings --quiet 'result(VList(.PyVals))'

# Include verification helpers in the Haskell definition, then prove every
# claim in spec.k in one positive target-proof command.
kompile verification.k \
  --main-module MPY-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --backend haskell \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
