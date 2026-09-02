#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py smoke.py > smoke.mpy

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun smoke.mpy --definition runtime-kompiled

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
  --spec-module SPEC-VACUITY
vacuity_probe_status=$?
set -e
if [[ ${vacuity_probe_status} -eq 0 ]]; then
  echo "ERROR: off-by-one mutation unexpectedly proved" >&2
  exit 1
fi
echo "EXPECTED FAILURE: off-by-one mutation exited ${vacuity_probe_status}"

set +e
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
body_probe_status=$?
set -e
if [[ ${body_probe_status} -eq 0 ]]; then
  echo "ERROR: mutated implementation unexpectedly proved" >&2
  exit 1
fi
echo "EXPECTED FAILURE: body mutation exited ${body_probe_status}"

python3 differential_test.py

python3 -c 'from solution import modp; print("negative-exponent-witness:", modp(-1, 5), type(modp(-1, 5)).__name__)'
python3 -c 'from solution import modp
try:
    modp(3, 0)
except Exception as err:
    print("zero-modulus-witness:", type(err).__name__, str(err))'
