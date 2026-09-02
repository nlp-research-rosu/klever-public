#!/usr/bin/env bash
set -euo pipefail

# Regenerate the transliteration from the submitted Python source.
python3 py2mpy.py solution.py > solution.mpy

# Cross-check the Python implementation itself, including the prompt example.
python3 - <<'PY'
from solution import remove_duplicates

assert remove_duplicates([1, 2, 3, 2, 4]) == [1, 3, 4]
assert remove_duplicates([]) == []
assert remove_duplicates([1, 1, 1]) == []
assert remove_duplicates([-1, 0, -1, 2]) == [0, 2]
PY

# Compile and exercise the semantics on concrete translated programs.
kompile semantic.k \
  --backend haskell \
  --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition semantic-kompiled
krun solution.mpy --definition semantic-kompiled \
  -cINPUT='listValue(1, 2, 3, 2, 4)'
krun solution.mpy --definition semantic-kompiled \
  -cINPUT='listValue()'
krun solution.mpy --definition semantic-kompiled \
  -cINPUT='listValue(-1, 0, -1, 2)'

# Compile the independent contract together with the semantics.
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

# First prove the generalized inductive iterator lemma.  Then use that already
# proved lemma compositionally while proving the exact translated program.
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims walk-correct
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --trusted walk-correct
