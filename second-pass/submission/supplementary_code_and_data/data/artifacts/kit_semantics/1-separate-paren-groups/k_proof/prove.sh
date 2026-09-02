#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy
python3 -m py_compile solution.py concrete-tests.py differential_test.py

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

python3 py2mpy.py concrete-tests.py > concrete-tests.mpy
krun concrete-tests.mpy --definition runtime-kompiled | tee concrete-krun.out
grep -A2 '<k>' concrete-krun.out | grep -q '\.K'
grep -A2 '<exit-code>' concrete-krun.out | grep -q '0'

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

# Required positive target proof: both claims in SPEC must close together.
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC

# Gate A5: a deliberately false result for witness "()" must be rejected.
if kprove spec-vacuity.k \
     --definition verification-kompiled \
     --spec-module SPEC-VACUITY
then
  echo "ERROR: false-result mutation unexpectedly proved" >&2
  exit 1
else
  vacuity_status=$?
  test "$vacuity_status" -eq 1
  echo "EXPECTED_FAILURE spec-vacuity.k exit=$vacuity_status"
fi

# Gate A1: changing the source body while retaining the correct result must fail.
if kprove spec-body-mutation.k \
     --definition verification-kompiled \
     --spec-module SPEC-BODY-MUTATION
then
  echo "ERROR: body mutation unexpectedly proved" >&2
  exit 1
else
  body_status=$?
  test "$body_status" -eq 1
  echo "EXPECTED_FAILURE spec-body-mutation.k exit=$body_status"
fi

python3 differential_test.py
