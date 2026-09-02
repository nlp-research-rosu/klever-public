#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy
sha256sum --check solution.mpy.sha256
python3 py2mpy.py concrete-tests.py > concrete-tests.mpy

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun concrete-tests.mpy --definition runtime-kompiled | tee concrete-krun.log

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC 2>&1 | tee proof-target.log

if kprove spec-vacuity.k \
    --definition verification-kompiled \
    --spec-module SPEC-VACUITY > proof-vacuity.log 2>&1; then
  cat proof-vacuity.log
  echo "ERROR: false-postcondition mutation unexpectedly proved"
  exit 1
else
  mutation_exit=$?
  cat proof-vacuity.log
  echo "EXPECTED_FAILURE: false-postcondition mutation exit ${mutation_exit}"
fi

if kprove spec-body-mutation.k \
    --definition verification-kompiled \
    --spec-module SPEC-BODY-MUTATION > proof-body-mutation.log 2>&1; then
  cat proof-body-mutation.log
  echo "ERROR: wrong-body mutation unexpectedly proved"
  exit 1
else
  mutation_exit=$?
  cat proof-body-mutation.log
  echo "EXPECTED_FAILURE: wrong-body mutation exit ${mutation_exit}"
fi

python3 differential_test.py | tee differential-test.log
