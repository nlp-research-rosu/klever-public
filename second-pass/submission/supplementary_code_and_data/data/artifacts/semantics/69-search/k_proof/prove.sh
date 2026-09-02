#!/usr/bin/env bash
set -euo pipefail

# Regenerate the required transliteration and confirm the concrete Python
# behavior against an exhaustive small-domain oracle.
python3 py2mpy.py solution.py > solution.mpy
python3 - <<'PY'
from itertools import product
from solution import search

def oracle(values):
    return max(
        (value for value in values
         if value > 0 and values.count(value) >= value),
        default=-1,
    )

for length in range(1, 7):
    for values in product(range(1, 7), repeat=length):
        values = list(values)
        assert search(values) == oracle(values), values
print("Python exhaustive oracle: passed")
PY

# Exercise the translated program and prompt examples with the required
# concrete LLVM definition.
python3 py2mpy.py smoke.py > smoke.mpy
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun smoke.mpy --definition runtime-kompiled --output none

# Compile the symbolic extension against MPY (not MPY-KRUN) and prove every
# claim in SEARCH-SPEC.  Success prints #Top and exits zero.
kompile verification.k \
  --backend haskell \
  --main-module SEARCH-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SEARCH-SPEC

# Expected-failure mutation probe: replacing == by != in the counting loop
# must not be covered by the source-specific proof accelerator.
if kprove mutation-spec.k \
     --definition verification-kompiled \
     --spec-module SEARCH-MUTATION-SPEC \
     > mutation.log 2>&1; then
  echo "Mutation unexpectedly proved" >&2
  exit 1
fi
rg -q "cannot be rewritten further" mutation.log
echo "K mutation rejection: passed"
