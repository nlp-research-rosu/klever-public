#!/usr/bin/env bash
set -u

overall=0
run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  if (( status != 0 )); then overall=1; fi
}

run /usr/bin/kompile \
  fixed-context-verification.k \
  --backend haskell \
  --main-module FIXED-CONTEXT-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition fixed-context-kompiled

printf '\nGround truth under supplied semantics only:\n'
run /usr/bin/kprove \
  fixed-context-spec.k \
  --definition fixed-context-kompiled \
  --spec-module FIXED-CONTEXT-SPEC

printf '\nFalse ground result under supplied semantics only (failure expected):\n'
printf '$ /usr/bin/kprove fixed-context-false-spec.k --definition fixed-context-kompiled --spec-module FIXED-CONTEXT-FALSE-SPEC\n'
/usr/bin/kprove \
  fixed-context-false-spec.k \
  --definition fixed-context-kompiled \
  --spec-module FIXED-CONTEXT-FALSE-SPEC \
  2>&1 | tee /audit-output/evidence/stage5_fixed_false_failure.log
status=${PIPESTATUS[0]}
printf '[exit %d; nonzero expected]\n' "$status"
if (( status == 0 )); then
  printf 'ERROR: supplied semantics proved false result 99\n'
  overall=1
fi
if ! rg -q 'WarnStuckClaimState|implication check.*failed|cannot be rewritten further' \
     /audit-output/evidence/stage5_fixed_false_failure.log; then
  printf 'ERROR: expected unmet-obligation diagnostic absent\n'
  overall=1
fi

exit "$overall"
