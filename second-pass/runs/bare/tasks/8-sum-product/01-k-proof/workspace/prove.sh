#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

# Recreate the constructor term from the submitted Python implementation.
python3 py2mpy.py solution.py > solution.mpy

# Check the Python implementation against the prompt examples and an edge case.
python3 - <<'PY'
from solution import sum_product

assert sum_product([]) == (0, 1)
assert sum_product([1, 2, 3, 4]) == (10, 24)
assert sum_product([-2, 0, 5]) == (3, 0)
print("Python checks passed")
PY

# Compile the executable semantics and exercise the translated program.
kompile semantic.k --backend llvm --main-module MPY --syntax-module MPY-SYNTAX

krun solution.mpy -cINPUT='PyList(.Ints)' \
  --definition semantic-kompiled \
  | grep -F 'PyTuple ( PyInt ( 0 ) , PyInt ( 1 ) )'

krun solution.mpy -cINPUT='PyList(1, 2, 3, 4, .Ints)' \
  --definition semantic-kompiled \
  | grep -F 'PyTuple ( PyInt ( 10 ) , PyInt ( 24 ) )'

krun solution.mpy -cINPUT='PyList(-2, 0, 5, .Ints)' \
  --definition semantic-kompiled \
  | grep -F 'PyTuple ( PyInt ( 3 ) , PyInt ( 0 ) )'

# Compile the proof semantics and prove the universal symbolic-list claim.
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX

kprove spec.k --definition verification-kompiled \
  --spec-module SUM-PRODUCT-SPEC | grep -x '#Top'
