#!/usr/bin/env bash
set +e

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

scratch=/tmp/audit-work/102-choose-num
definition="$scratch/body-mutation-kompiled"
verification="$scratch/verification-body-mutation.k"
spec="$scratch/spec-body-mutation.k"

printf 'Stage 5 operational body-sensitivity mutation\n'
run cp /audit-output/evidence/verification-body-mutation.k "$verification"
run cp /audit-output/evidence/spec-body-mutation.k "$spec"
run test ! -e "$definition"
run kompile "$verification" \
  --backend haskell \
  --main-module CHOOSE-NUM-VERIFICATION-BODY-MUTATION \
  --syntax-module MPY-SYNTAX \
  --output-definition "$definition"
run kprove "$spec" \
  --definition "$definition" \
  --spec-module CHOOSE-NUM-SPEC-BODY-MUTATION \
  --dry-run
run kprove "$spec" \
  --definition "$definition" \
  --spec-module CHOOSE-NUM-SPEC-BODY-MUTATION \
  --claims CHOOSE-NUM-SPEC-BODY-MUTATION.mutated-body-must-not-prove-original-result
