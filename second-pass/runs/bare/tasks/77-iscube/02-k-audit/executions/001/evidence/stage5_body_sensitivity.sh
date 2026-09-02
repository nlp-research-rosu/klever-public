#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/77-iscube
mutant="$scratch/body-mutant"
definition="$scratch/audit-body-mutant-kompiled"

printf '%s\n' 'Mutation: final source-tree comparison CmpOp("==", Name("a")) becomes CmpOp("<", Name("a")).'
printf '%s\n' '$ diff -u candidate-src/verification.k body-mutant/verification.k'
diff -u "$scratch/candidate-src/verification.k" "$mutant/verification.k"
diff_status=$?
printf '[exit %d; 1 is expected because the mutation differs]\n' "$diff_status"

printf '\n$ test ! -e %q\n' "$definition"
test ! -e "$definition"
precheck_status=$?
printf '[exit %d]\n' "$precheck_status"

printf '\n$ kompile %q --main-module VERIFICATION --syntax-module VERIFICATION --backend haskell --output-definition %q\n' \
  "$mutant/verification.k" "$definition"
kompile "$mutant/verification.k" \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION \
  --backend haskell \
  --output-definition "$definition"
build_status=$?
printf '[exit %d]\n' "$build_status"

printf '\n$ kprove %q --definition %q --spec-module CUBE-SPEC --exclude CUBE-SPEC.negative-cube\n' \
  "$mutant/spec.k" "$definition"
proof_output="$(
  kprove "$mutant/spec.k" \
    --definition "$definition" \
    --spec-module CUBE-SPEC \
    --exclude CUBE-SPEC.negative-cube 2>&1
)"
proof_status=$?
printf '%s\n' "$proof_output"
printf '[exit %d; nonzero is expected]\n' "$proof_status"

if (( build_status == 0 && proof_status != 0 )) \
  && grep -q 'WarnStuckClaimState' <<<"$proof_output"; then
  printf '%s\n' 'BODY_SENSITIVITY=PASS'
  exit 0
fi

printf '%s\n' 'BODY_SENSITIVITY=FAIL'
exit 1
