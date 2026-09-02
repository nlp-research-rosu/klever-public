#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete_tests.py > concrete_tests.mpy
python3 py2mpy.py body_mutation.py > body_mutation.mpy

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun concrete_tests.mpy --definition runtime-kompiled

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

# Supporting isolated invariant proof.
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.loop-inv

# Required positive target proof: both the invariant and whole entry claim.
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC

kompile --backend haskell connection.k \
  --main-module CONNECTION \
  --syntax-module MPY-SYNTAX \
  --output-definition connection-kompiled

# Bridge-free universal fixed-semantics equations used to justify the guarded
# dynamic dispatch twins.
kprove connection-spec.k \
  --definition connection-kompiled \
  --spec-module CONNECTION-SPEC

if kprove spec-vacuity.k \
     --definition verification-kompiled \
     --spec-module SPEC-VACUITY; then
  echo "UNEXPECTED: false-result mutation proved"
  exit 1
else
  echo "EXPECTED FAILURE: false-result mutation was rejected"
fi

if krun body_mutation.mpy --definition runtime-kompiled; then
  echo "UNEXPECTED: material body mutant passed"
  exit 1
else
  echo "EXPECTED FAILURE: material body mutant changed the result"
fi

python3 differential_test.py
