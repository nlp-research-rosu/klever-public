#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete_tests.py > concrete_tests.mpy
python3 py2mpy.py model_boundary.py > model_boundary.mpy
python3 differential_test.py

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun solution.mpy --definition runtime-kompiled
krun concrete_tests.mpy --definition runtime-kompiled
krun model_boundary.mpy --definition runtime-kompiled
python3 model_boundary_cpython.py

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
  > vacuity-probe.log 2>&1
vacuity_status=$?
set -e
cat vacuity-probe.log
if [[ $vacuity_status -ne 1 ]]; then
  echo "Unexpected vacuity-probe exit: $vacuity_status" >&2
  exit 1
fi
echo "EXPECTED FAILURE: false-result probe exited 1"

set +e
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION \
  > body-mutation-probe.log 2>&1
body_mutation_status=$?
set -e
cat body-mutation-probe.log
if [[ $body_mutation_status -ne 1 ]]; then
  echo "Unexpected body-mutation-probe exit: $body_mutation_status" >&2
  exit 1
fi
echo "EXPECTED FAILURE: changed-body probe exited 1"
