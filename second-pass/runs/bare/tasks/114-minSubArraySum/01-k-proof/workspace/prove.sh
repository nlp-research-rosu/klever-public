#!/usr/bin/env bash
set -euo pipefail

# Regenerate the constructor term from the submitted Python implementation.
python3 py2mpy.py solution.py > solution.mpy
python3 -m py_compile solution.py

# Independent executable testing of the Python implementation against the
# direct definition, exhaustively over 19,607 small non-empty lists.
python3 - <<'PY'
from itertools import product
from solution import minSubArraySum

def reference(xs):
    return min(sum(xs[i:j])
               for i in range(len(xs))
               for j in range(i + 1, len(xs) + 1))

checked = 0
for size in range(1, 6):
    for xs in product(range(-3, 4), repeat=size):
        assert minSubArraySum(list(xs)) == reference(xs)
        checked += 1
print(f"Python exhaustive checks passed: {checked}")
PY

# Build and concretely exercise the handwritten semantics on the prompt's two
# examples and a singleton/base case.
kompile semantic.k --backend haskell --main-module MPY --syntax-module MPY-SYNTAX
krun solution.mpy --definition semantic-kompiled \
  -cENTRY='"minSubArraySum"' \
  -cARGS='pyList(cons(2, cons(3, cons(4, cons(1, cons(2, cons(4, nil)))))))'
krun solution.mpy --definition semantic-kompiled \
  -cENTRY='"minSubArraySum"' \
  -cARGS='pyList(cons(-1, cons(-2, cons(-3, nil))))'
krun solution.mpy --definition semantic-kompiled \
  -cENTRY='"minSubArraySum"' \
  -cARGS='pyList(cons(7, nil))'

# Compile the semantics together with the mathematical verification functions,
# then prove every claim in spec.k.  Success prints #Top and exits zero.
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX
kprove spec.k --definition verification-kompiled
