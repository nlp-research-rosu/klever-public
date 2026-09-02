#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete-tests.py > concrete-tests.mpy
python3 validate_artifacts.py
python3 differential_test.py

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun concrete-tests.mpy \
  --definition runtime-kompiled \
  --output none
echo "concrete krun: PASS"

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC

if kprove spec-vacuity.k \
     --definition verification-kompiled \
     --spec-module SPEC-VACUITY
then
  echo "unexpected success: false-postcondition mutation"
  exit 1
else
  echo "false-postcondition mutation: EXPECTED FAILURE"
fi

if kprove spec-body-mutation.k \
     --definition verification-kompiled \
     --spec-module SPEC-BODY-MUTATION
then
  echo "unexpected success: changed-body mutation"
  exit 1
else
  echo "changed-body mutation: EXPECTED FAILURE"
fi
