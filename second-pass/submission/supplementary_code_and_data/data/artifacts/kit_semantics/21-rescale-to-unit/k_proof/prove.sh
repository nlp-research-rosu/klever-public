#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy
python3 evidence.py | tee evidence.log

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

python3 py2mpy.py concrete_test.py > concrete_test.mpy
krun concrete_test.mpy --definition runtime-kompiled > concrete-test.log
rg -U -q '<k>\s*\.K\s*</k>' concrete-test.log
rg -U -q '<exc>\s*NoExc\s*</exc>' concrete-test.log
rg -U -q '<exit-code>\s*0\s*</exit-code>' concrete-test.log

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC | tee target-proof.log
rg -x -q '#Top' target-proof.log

sed \
  -e 's/^module SPEC$/module SPEC-VACUITY/' \
  -e 's/=> ref(0)/=> noneV/' \
  spec.k > spec-vacuity.k

if kprove spec-vacuity.k \
     --definition verification-kompiled \
     --spec-module SPEC-VACUITY > vacuity.log 2>&1; then
  echo "ERROR: false-return mutation unexpectedly proved" >&2
  exit 1
else
  vacuity_status=$?
  echo "expected vacuity failure: exit ${vacuity_status}"
fi
rg -q 'WarnStuckClaimState' vacuity.log
rg -U -q '<k>\s*ref \( 0 \) ~> \.K\s*</k>' vacuity.log

sed \
  -e 's/^module SPEC$/module SPEC-BODY-MUTATION/' \
  -e 's/Return(Name("result"))/Return(Name("numbers"))/g' \
  spec.k > spec-body-mutation.k

if kprove spec-body-mutation.k \
     --definition verification-kompiled \
     --spec-module SPEC-BODY-MUTATION > body-mutation.log 2>&1; then
  echo "ERROR: changed-body mutation unexpectedly proved" >&2
  exit 1
else
  body_status=$?
  echo "expected body-mutation failure: exit ${body_status}"
fi
rg -q 'WarnStuckClaimState' body-mutation.log
rg -U -q '<k>\s*list \(' body-mutation.log
