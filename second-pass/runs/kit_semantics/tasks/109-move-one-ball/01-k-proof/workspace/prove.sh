#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete_tests.py > concrete_tests.mpy
python3 py2mpy.py solution.py | cmp - solution.mpy

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun concrete_tests.mpy --definition runtime-kompiled

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.scan-loop

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC

set +e
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
vacuity_status=$?
set -e
if [[ "$vacuity_status" -eq 0 ]]; then
  echo "ERROR: false-postcondition mutation unexpectedly proved"
  exit 1
fi
echo "EXPECTED FAILURE: false-postcondition mutation exit $vacuity_status"

set +e
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
body_status=$?
set -e
if [[ "$body_status" -eq 0 ]]; then
  echo "ERROR: body mutation unexpectedly proved"
  exit 1
fi
echo "EXPECTED FAILURE: body mutation exit $body_status"

python3 differential_tests.py
