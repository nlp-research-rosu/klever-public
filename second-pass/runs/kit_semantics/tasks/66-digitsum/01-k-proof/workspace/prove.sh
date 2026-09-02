#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py smoke.py > smoke.mpy
python3 py2mpy.py body_mutation.py > body_mutation.mpy

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun smoke.mpy --definition runtime-kompiled | tee krun-smoke.log
krun body_mutation.mpy --definition runtime-kompiled \
  | tee krun-body-mutation.log
python3 differential_test.py | tee differential.log

kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  | tee proof-positive.log

set +e
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY \
  2>&1 | tee proof-vacuity.log
vacuity_probe_status=${PIPESTATUS[0]}

kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION \
  2>&1 | tee proof-body-mutation.log
body_probe_status=${PIPESTATUS[0]}
set -e

if [[ ${vacuity_probe_status} -eq 0 ]]; then
  echo "ERROR: the false-postcondition probe unexpectedly proved"
  exit 1
fi

if [[ ${body_probe_status} -eq 0 ]]; then
  echo "ERROR: the body-sensitivity probe unexpectedly proved"
  exit 1
fi

echo "Expected-failure probes rejected as required."
