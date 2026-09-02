#!/usr/bin/env bash
set -euo pipefail

# Regenerate both constructor programs with the fixed translator.
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete_tests.py > concrete_tests.mpy

# Differentially check the Python implementation against the direct contract.
python3 - <<'PY'
import random
from solution import next_smallest

rng = random.Random(20260723)
for _ in range(2000):
    values = [rng.randint(-20, 20) for _ in range(rng.randint(0, 30))]
    distinct = sorted(set(values))
    expected = distinct[1] if len(distinct) >= 2 else None
    assert next_smallest(values) == expected, (values, expected)
print("Python differential tests passed")
PY

# Concrete execution uses the supplied runtime semantics and its LLVM-only leg.
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete_tests.mpy --definition runtime-kompiled

# First prove the universal loop theorem directly from MPY.
kompile verification.k \
  --backend haskell \
  --main-module NEXT-SMALLEST-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module NEXT-SMALLEST-LOOP-SPEC \
  | tee loop-proof.out
rg -x '#Top' loop-proof.out

# Then install that proved theorem as a lemma and prove the public entry call.
kompile verification.k \
  --backend haskell \
  --main-module NEXT-SMALLEST-WITH-LOOP-LEMMA \
  --syntax-module MPY-SYNTAX \
  --output-definition entry-verification-kompiled
kprove spec.k \
  --definition entry-verification-kompiled \
  --spec-module NEXT-SMALLEST-ENTRY-SPEC \
  | tee entry-proof.out
rg -x '#Top' entry-proof.out
