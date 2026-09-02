#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py solution.py | diff - solution.mpy
python3 py2mpy.py concrete-tests.py > concrete-tests.mpy

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete-tests.mpy --definition runtime-kompiled

python3 differential_test.py

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.loop-inv
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC

set +e
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
VACUITY_PROBE_STATUS=$?
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
BODY_MUTATION_PROBE_STATUS=$?
set -e

if [[ $VACUITY_PROBE_STATUS -eq 0 ]]; then
  echo "ERROR: false-result mutation unexpectedly proved"
  exit 1
fi
if [[ $BODY_MUTATION_PROBE_STATUS -eq 0 ]]; then
  echo "ERROR: mutated body unexpectedly proved the original result"
  exit 1
fi

echo "Expected-failure probes rejected:"
echo "  spec-vacuity.k exit $VACUITY_PROBE_STATUS"
echo "  spec-body-mutation.k exit $BODY_MUTATION_PROBE_STATUS"
