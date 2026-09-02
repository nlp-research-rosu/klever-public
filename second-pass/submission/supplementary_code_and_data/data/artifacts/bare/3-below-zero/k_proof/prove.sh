#!/usr/bin/env bash
set -euo pipefail

# Recreate the constructor term from the unmodified fixed translator.
python3 py2mpy.py solution.py > solution.mpy
printf '%s  %s\n' \
  '9ffee3cf630e5a15d0fc1e32c990a029e920330f41b306516f1bcc0b5d44219d' \
  'solution.mpy' | sha256sum --check -

# Sanity-check the Python implementation on the prompt examples and boundary
# cases before exercising the translated term.
python3 - <<'PY'
from solution import below_zero

cases = [
    ([], False),
    ([1, 2, 3], False),
    ([1, 2, -4, 5], True),
    ([-1], True),
    ([5, -5], False),
]
for operations, expected in cases:
    assert below_zero(operations) is expected
PY

# LLVM gives fast concrete execution of the generated solution.mpy.
kompile semantic.k \
  --backend llvm \
  --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --output-definition semantic-llvm

krun solution.mpy -d semantic-llvm \
  -cOPERATIONS='cons(1, cons(2, cons(3, .IntList)))'
krun solution.mpy -d semantic-llvm \
  -cOPERATIONS='cons(1, cons(2, cons(-4, cons(5, .IntList))))'

# The Haskell backend proves the two compositional claims.  Together they say
# that the exact translated module reaches the loop cut-point, and that the
# loop returns the independent recursive prefix-sum specification for every
# IntList.
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-haskell

kprove spec.k -d verification-haskell \
  --spec-module SPEC \
  --claims SPEC.entry-reaches-loop
kprove spec.k -d verification-haskell \
  --spec-module SPEC \
  --claims SPEC.loop-correct
