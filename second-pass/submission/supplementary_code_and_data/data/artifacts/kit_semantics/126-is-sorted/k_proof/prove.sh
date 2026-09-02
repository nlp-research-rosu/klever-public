#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py smoke.py > smoke.mpy
python3 py2mpy.py sort_smoke.py > sort_smoke.mpy

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun smoke.mpy --definition runtime-kompiled > krun-smoke.out
krun sort_smoke.mpy --definition runtime-kompiled > krun-sort.out
python3 differential_test.py

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC

set +e
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY \
  --claims SPEC-VACUITY.entry-false-empty
mutation_status=$?
set -e

if [[ "$mutation_status" -eq 0 ]]; then
  echo "ERROR: false-postcondition mutation unexpectedly proved"
  exit 1
fi

echo "EXPECTED FAILURE: false-postcondition mutation exit=$mutation_status"
