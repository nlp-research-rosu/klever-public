#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete_test.py > concrete_test.mpy
python3 -m py_compile solution.py

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun concrete_test.mpy --definition runtime-kompiled
python3 test_solution.py

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC

if kprove spec-vacuity.k \
    --definition verification-kompiled \
    --spec-module SPEC-VACUITY; then
  echo "ERROR: false-postcondition probe unexpectedly proved" >&2
  exit 1
else
  status=$?
  echo "EXPECTED FAILURE: false-postcondition probe exited ${status}"
fi

if kprove spec-body-mutation.k \
    --definition verification-kompiled \
    --spec-module SPEC-BODY-MUTATION; then
  echo "ERROR: body-mutation probe unexpectedly proved" >&2
  exit 1
else
  status=$?
  echo "EXPECTED FAILURE: body-mutation probe exited ${status}"
fi
