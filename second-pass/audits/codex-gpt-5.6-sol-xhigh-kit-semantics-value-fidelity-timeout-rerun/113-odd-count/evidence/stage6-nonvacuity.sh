#!/usr/bin/env bash
set -u

SPEC=/audit-output/evidence/fresh-false-spec.k
DEFINITION=/tmp/audit-work/build/verification-kompiled
status=0

printf 'Fresh false mutation witness: INPUT=.ValSeq satisfies allStringValues; actual output is [], demanded output is [None].\n'

printf '$ kprove %s --definition %s --spec-module FRESH-FALSE-SPEC --dry-run\n' \
  "$SPEC" "$DEFINITION"
kprove "$SPEC" \
  --definition "$DEFINITION" \
  --spec-module FRESH-FALSE-SPEC \
  --dry-run \
  > /audit-output/evidence/stage6-false-dry-run.log 2>&1
dry_rc=$?
printf '[exit %d]\n' "$dry_rc"
tail -100 /audit-output/evidence/stage6-false-dry-run.log
if (( dry_rc != 0 )); then status=1; fi

printf '$ kprove %s --definition %s --spec-module FRESH-FALSE-SPEC\n' \
  "$SPEC" "$DEFINITION"
kprove "$SPEC" \
  --definition "$DEFINITION" \
  --spec-module FRESH-FALSE-SPEC \
  > /audit-output/evidence/stage6-false-kprove.log 2>&1
prove_rc=$?
printf '[exit %d; expected nonzero]\n' "$prove_rc"
tail -220 /audit-output/evidence/stage6-false-kprove.log
if (( prove_rc == 0 )); then status=1; fi
if ! rg -q 'WarnStuckClaimState' /audit-output/evidence/stage6-false-kprove.log; then
  status=1
fi
if ! rg -Fq '0 |-> list ( .ValSeq )' /audit-output/evidence/stage6-false-kprove.log; then
  status=1
fi

printf 'Final nonvacuity_status=%d\n' "$status"
exit "$status"
