#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

kompile --version
kprove --version

python3 py2mpy.py solution.py > solution.mpy
python3 -m py_compile solution.py

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

python3 py2mpy.py concrete_tests.py > concrete_tests.mpy
krun concrete_tests.mpy --definition runtime-kompiled

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.hex-loop

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.hex-key,SPEC.hex-loop \
  --trusted SPEC.hex-loop

python3 test_solution.py

if kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY \
  --claims SPEC-VACUITY.hex-key-off-by-one,SPEC.hex-loop \
  --trusted SPEC.hex-loop
then
  echo "UNEXPECTED SUCCESS: false off-by-one postcondition"
  exit 1
else
  echo "EXPECTED FAILURE: false off-by-one postcondition"
fi

if kprove spec-value-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-VALUE-MUTATION \
  --claims SPEC-VALUE-MUTATION.two-is-zero,SPEC.hex-loop \
  --trusted SPEC.hex-loop
then
  echo "UNEXPECTED SUCCESS: wrong ground value for input 2"
  exit 1
else
  echo "EXPECTED FAILURE: wrong ground value for input 2"
fi

if kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION \
  --claims SPEC-BODY-MUTATION.starts-at-one,SPEC.hex-loop \
  --trusted SPEC.hex-loop
then
  echo "UNEXPECTED SUCCESS: mutated initial accumulator"
  exit 1
else
  echo "EXPECTED FAILURE: mutated initial accumulator"
fi

if kprove spec-loop-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-LOOP-BODY-MUTATION \
  --claims SPEC-LOOP-BODY-MUTATION.d-is-still-counted,SPEC.hex-loop \
  --trusted SPEC.hex-loop
then
  echo "UNEXPECTED SUCCESS: mutated loop membership literal"
  exit 1
else
  echo "EXPECTED FAILURE: mutated loop membership literal"
fi
