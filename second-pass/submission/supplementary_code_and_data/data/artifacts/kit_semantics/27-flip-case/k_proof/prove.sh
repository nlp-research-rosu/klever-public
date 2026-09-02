#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py smoke.py > smoke.mpy
python3 py2mpy.py model_boundary.py > model_boundary.mpy
python3 -m py_compile solution.py test_solution.py

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun solution.mpy --definition runtime-kompiled
krun smoke.mpy --definition runtime-kompiled
python3 test_solution.py

# Expected model-boundary failure: the supplied semantics only constructs
# ASCII characters, whereas CPython strings and swapcase are Unicode-aware.
set +e
krun model_boundary.mpy --definition runtime-kompiled
boundary_status=$?
set -e
printf 'MODEL_BOUNDARY_EXIT=%s (expected non-zero)\n' "$boundary_status"
if [[ "$boundary_status" -eq 0 ]]; then
  echo "ERROR: the non-ASCII model-boundary probe unexpectedly succeeded" >&2
  exit 1
fi
python3 -c 'print("CPython boundary:", "é".swapcase(), [ord(c) for c in "é".swapcase()])'

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

# Required positive, full-domain target proof.
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC

# Expected Gate A failures: the proof must reject a false result and a
# materially changed function body.
set +e
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
vacuity_status=$?
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
body_status=$?
set -e

printf 'VACUITY_EXIT=%s (expected non-zero)\n' "$vacuity_status"
printf 'BODY_MUTATION_EXIT=%s (expected non-zero)\n' "$body_status"
if [[ "$vacuity_status" -eq 0 || "$body_status" -eq 0 ]]; then
  echo "ERROR: a negative proof probe unexpectedly succeeded" >&2
  exit 1
fi
