#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

python3 py2mpy.py smoke.py > smoke.mpy
python3 smoke.py
krun smoke.mpy --definition runtime-kompiled
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
  > vacuity-probe.log 2>&1
vacuity_status=$?

kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION \
  > body-mutation-probe.log 2>&1
body_status=$?
set -e

cat vacuity-probe.log
echo "vacuity probe exit: ${vacuity_status} (expected non-zero)"
cat body-mutation-probe.log
echo "body mutation probe exit: ${body_status} (expected non-zero)"

if [[ ${vacuity_status} -eq 0 || ${body_status} -eq 0 ]]; then
  echo "A required negative validation probe unexpectedly passed." >&2
  exit 1
fi
