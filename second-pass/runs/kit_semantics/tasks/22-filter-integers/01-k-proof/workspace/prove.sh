#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete-tests.py > concrete-tests.mpy
python3 differential-test.py

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun concrete-tests.mpy --definition runtime-kompiled \
  | tee concrete-tests.krun.out
rg -U '<k>\s*\.K\s*</k>' concrete-tests.krun.out
rg -U '<exc>\s*NoExc\s*</exc>' concrete-tests.krun.out
rg -U '<exit-code>\s*0\s*</exit-code>' concrete-tests.krun.out

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  | tee target.kprove.out
rg '^#Top$' target.kprove.out

if kprove spec-vacuity.k \
     --definition verification-kompiled \
     --spec-module SPEC-VACUITY \
     > spec-vacuity.kprove.out 2>&1
then
  echo "ERROR: false-result mutation unexpectedly proved" >&2
  exit 1
else
  mutation_status=$?
  cat spec-vacuity.kprove.out
  rg 'WarnStuckClaimState' spec-vacuity.kprove.out
  echo "false-result mutation: expected exit ${mutation_status}"
fi

if kprove spec-body-mutation.k \
     --definition verification-kompiled \
     --spec-module SPEC-BODY-MUTATION \
     > spec-body-mutation.kprove.out 2>&1
then
  echo "ERROR: body mutation unexpectedly proved" >&2
  exit 1
else
  mutation_status=$?
  cat spec-body-mutation.kprove.out
  rg 'WarnStuckClaimState' spec-body-mutation.kprove.out
  echo "body mutation: expected exit ${mutation_status}"
fi

if kprove spec-classifier-mutation.k \
     --definition verification-kompiled \
     --spec-module SPEC-CLASSIFIER-MUTATION \
     > spec-classifier-mutation.kprove.out 2>&1
then
  echo "ERROR: integer-discarded mutation unexpectedly proved" >&2
  exit 1
else
  mutation_status=$?
  cat spec-classifier-mutation.kprove.out
  rg 'WarnStuckClaimState' spec-classifier-mutation.kprove.out
  echo "integer-discarded mutation: expected exit ${mutation_status}"
fi

if kprove spec-noninteger-mutation.k \
     --definition verification-kompiled \
     --spec-module SPEC-NONINTEGER-MUTATION \
     > spec-noninteger-mutation.kprove.out 2>&1
then
  echo "ERROR: string-retained mutation unexpectedly proved" >&2
  exit 1
else
  mutation_status=$?
  cat spec-noninteger-mutation.kprove.out
  rg 'WarnStuckClaimState' spec-noninteger-mutation.kprove.out
  echo "string-retained mutation: expected exit ${mutation_status}"
fi
