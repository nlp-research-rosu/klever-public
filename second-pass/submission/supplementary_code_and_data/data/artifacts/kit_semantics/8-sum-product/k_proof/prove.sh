#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

python3 py2mpy.py solution.py > solution.mpy
cmp solution.mpy <(python3 py2mpy.py solution.py)

python3 py2mpy.py smoke.py > smoke.mpy

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition semantics-kompiled

krun smoke.mpy --definition semantics-kompiled

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC

python3 test_solution.py

set +e
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
vacuity_status=$?

kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
body_mutation_status=$?
set -e

echo "VACUITY_EXIT=$vacuity_status (expected non-zero)"
echo "BODY_MUTATION_EXIT=$body_mutation_status (expected non-zero)"

if [[ $vacuity_status -eq 0 || $body_mutation_status -eq 0 ]]; then
  echo "A negative validation probe unexpectedly proved." >&2
  exit 1
fi
