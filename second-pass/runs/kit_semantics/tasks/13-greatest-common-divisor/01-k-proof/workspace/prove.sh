#!/bin/sh
set -eu

python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete.py > concrete.mpy
python3 -m py_compile solution.py test_solution.py
python3 py2mpy.py solution.py | diff -u solution.mpy -

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun solution.mpy --definition runtime-kompiled
krun concrete.mpy --definition runtime-kompiled
python3 test_solution.py

kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.gcd-loop

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.gcd-entry

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC

if kprove spec-vacuity.k \
    --definition verification-kompiled \
    --spec-module SPEC-VACUITY
then
  echo "UNEXPECTED SUCCESS: false-result mutation proved"
  exit 1
else
  probe_status=$?
  echo "EXPECTED FAILURE: false-result mutation exit ${probe_status}"
fi

if kprove spec-body-mutation.k \
    --definition verification-kompiled \
    --spec-module SPEC-BODY-MUTATION
then
  echo "UNEXPECTED SUCCESS: body mutation proved"
  exit 1
else
  probe_status=$?
  echo "EXPECTED FAILURE: body mutation exit ${probe_status}"
fi
