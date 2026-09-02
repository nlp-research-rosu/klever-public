#!/usr/bin/env bash
set -u

work=/tmp/audit-work/reconstruction
evidence=/audit-output/evidence
status=0

printf 'STAGE 6 FRESH FALSE-POSTCONDITION NON-VACUITY TEST\n'
printf 'Satisfying witness: list(vCons(1,.ValSeq)), threshold 2; 1 < 2, so actual result is true.\n'

printf '\n$ cd %q && kprove stage6-false-postcondition.k --definition fresh-verification-kompiled --spec-module STAGE6-FALSE-POSTCONDITION --dry-run\n' "$work"
(cd "$work" && kprove stage6-false-postcondition.k \
  --definition fresh-verification-kompiled \
  --spec-module STAGE6-FALSE-POSTCONDITION \
  --dry-run) > "$evidence/stage6-false-postcondition-dry-run.log" 2>&1
dry_rc=$?
sed -n '1,200p' "$evidence/stage6-false-postcondition-dry-run.log"
printf '[exit %d; required 0]\n' "$dry_rc"
if [ "$dry_rc" -ne 0 ]; then
  status=1
fi

printf '\n$ cd %q && kprove stage6-false-postcondition.k --definition fresh-verification-kompiled --spec-module STAGE6-FALSE-POSTCONDITION\n' "$work"
(cd "$work" && kprove stage6-false-postcondition.k \
  --definition fresh-verification-kompiled \
  --spec-module STAGE6-FALSE-POSTCONDITION) \
  > "$evidence/stage6-false-postcondition-kprove.log" 2>&1
prove_rc=$?
sed -n '1,240p' "$evidence/stage6-false-postcondition-kprove.log"
printf '[exit %d; required nonzero]\n' "$prove_rc"
if [ "$prove_rc" -eq 0 ]; then
  status=1
fi

printf '\n$ rg -n %q %q\n' \
  'WarnStuckClaimState|true|false|cannot be rewritten further' \
  "$evidence/stage6-false-postcondition-kprove.log"
rg -n 'WarnStuckClaimState|true|false|cannot be rewritten further' \
  "$evidence/stage6-false-postcondition-kprove.log"
rg_rc=$?
printf '[exit %d]\n' "$rg_rc"
if [ "$rg_rc" -ne 0 ]; then
  status=1
fi

exit "$status"
