#!/usr/bin/env bash
set -u

WORK=/tmp/audit-work/candidate-src
BUILD=/tmp/audit-work/build-body-mutation-final

cp /audit-output/evidence/verification-body-mutation.k \
  "$WORK/verification-body-mutation.k"
cp /audit-output/evidence/spec-body-mutation.k \
  "$WORK/spec-body-mutation.k"
cp /audit-output/evidence/program-body-mutation.mpy \
  "$WORK/program-body-mutation.mpy"
mkdir -p "$BUILD"

printf '%s\n' \
  'COMMAND: kompile verification-body-mutation.k --backend haskell --main-module VERIFICATION-BODY-MUTATION --syntax-module MPY-SYNTAX --output-definition /tmp/audit-work/build-body-mutation-final/verification-kompiled'
timeout 300 kompile verification-body-mutation.k \
  --backend haskell \
  --main-module VERIFICATION-BODY-MUTATION \
  --syntax-module MPY-SYNTAX \
  --output-definition "$BUILD/verification-kompiled"
compile_status=$?
printf 'BODY_MUTATION_KOMPILE_EXIT_STATUS=%s\n' "$compile_status"
if [[ "$compile_status" -ne 0 ]]; then
  exit "$compile_status"
fi

printf '%s\n' \
  'COMMAND: krun program-body-mutation.mpy --definition /tmp/audit-work/build-body-mutation-final/verification-kompiled -cINPUT=pyList(intCons(1,nil))'
krun program-body-mutation.mpy \
  --definition "$BUILD/verification-kompiled" \
  -cINPUT='pyList(intCons(1,nil))'
krun_status=$?
printf 'BODY_MUTATION_KRUN_EXIT_STATUS=%s\n' "$krun_status"
if [[ "$krun_status" -ne 0 ]]; then
  exit "$krun_status"
fi

printf '%s\n' \
  'COMMAND: kprove spec-body-mutation.k --definition /tmp/audit-work/build-body-mutation-final/verification-kompiled --spec-module SPEC-BODY-MUTATION'
timeout 300 kprove spec-body-mutation.k \
  --definition "$BUILD/verification-kompiled" \
  --spec-module SPEC-BODY-MUTATION
proof_status=$?
printf 'BODY_MUTATION_KPROVE_EXIT_STATUS=%s\n' "$proof_status"
if [[ "$proof_status" -eq 0 ]]; then
  printf '%s\n' 'BODY_SENSITIVITY_RESULT=FAIL_UNEXPECTED_PROOF'
  exit 1
fi
printf '%s\n' 'BODY_SENSITIVITY_RESULT=PASS_EXPECTED_REJECTION'
exit 0
