#!/usr/bin/env bash
set -eu

kompile --version
kprove --version

python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete_tests.py > concrete_tests.mpy

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun solution.mpy --definition runtime-kompiled
krun concrete_tests.mpy --definition runtime-kompiled
python3 differential_test.py

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
echo "POSITIVE PROOF EXIT: 0"

set +e
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
vacuity_status=$?
set -e
if [ "$vacuity_status" -eq 0 ]
then
  echo "ERROR: false-postcondition mutation unexpectedly proved" >&2
  exit 1
else
  echo "EXPECTED FAILURE: false-postcondition mutation exited $vacuity_status"
fi

set +e
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
body_status=$?
set -e
if [ "$body_status" -eq 0 ]
then
  echo "ERROR: mutated-body claim unexpectedly proved" >&2
  exit 1
else
  echo "EXPECTED FAILURE: mutated-body claim exited $body_status"
fi
