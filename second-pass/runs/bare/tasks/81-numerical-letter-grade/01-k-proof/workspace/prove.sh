#!/usr/bin/env bash
set -euo pipefail

# Recreate the submitted K-constructor program from the submitted Python.
python3 py2mpy.py solution.py > solution.mpy

# Check the Python entry point against the prompt's example.
python3 - <<'PY'
from solution import numerical_letter_grade

assert numerical_letter_grade([4.0, 3, 1.7, 2, 3.5]) == [
    "A+", "B", "C-", "C", "A-"
]
PY

# Compile the semantics together with the independent verification model.
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX

# Execute the actual generated solution.mpy on the prompt's example.
krun solution.mpy \
  --definition verification-kompiled \
  -cINPUT='num(4,1) :: num(3,1) :: num(17,10) :: num(2,1) :: num(35,10) :: .Vals'

# Execute strict thresholds and endpoint cases in one traversal.
krun solution.mpy \
  --definition verification-kompiled \
  -cINPUT='num(4,1) :: num(38,10) :: num(37,10) :: num(33,10) :: num(30,10) :: num(27,10) :: num(23,10) :: num(20,10) :: num(17,10) :: num(13,10) :: num(10,10) :: num(7,10) :: num(0,1) :: .Vals'

# Prove every reachability claim in spec.k. Success prints #Top.
kprove spec.k --definition verification-kompiled
