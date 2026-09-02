#!/usr/bin/env bash
set -u
set -o pipefail

cd /tmp/audit-work/147-get-max-triples-clean || exit 1
status=0

printf '$ test ! -e /candidate/spec-vacuity.k\n'
test ! -e /candidate/spec-vacuity.k
rc=$?
printf '[exit %d; no candidate mutation present]\n' "$rc"
if (( rc != 0 )); then
  printf '[candidate mutation exists but remains untrusted]\n'
fi

printf '$ cp /audit-output/evidence/spec-vacuity.k scratch/spec-vacuity.k\n'
cp /audit-output/evidence/spec-vacuity.k ./spec-vacuity.k
printf '[exit 0]\n'

printf '$ kprove spec-vacuity.k --dry-run (parse/build gate)\n'
kprove spec-vacuity.k \
  --definition verification-audit-kompiled \
  --spec-module SPEC-VACUITY \
  --dry-run \
  -I . \
  --output pretty \
  > /audit-output/evidence/kprove-vacuity-dry-run.log 2>&1
dry_rc=$?
cat /audit-output/evidence/kprove-vacuity-dry-run.log
printf '[exit %d]\n' "$dry_rc"
if (( dry_rc != 0 )); then
  status=1
fi

printf '$ kprove spec-vacuity.k (expected semantic proof failure)\n'
kprove spec-vacuity.k \
  --definition verification-audit-kompiled \
  --spec-module SPEC-VACUITY \
  -I . \
  --output pretty \
  > /audit-output/evidence/kprove-vacuity.log 2>&1
proof_rc=$?
cat /audit-output/evidence/kprove-vacuity.log
printf '[exit %d]\n' "$proof_rc"

if (( proof_rc == 0 )); then
  printf '[unexpected success: false result 2 proved for N=5]\n'
  status=1
elif ! rg -q 'WarnStuckClaimState' /audit-output/evidence/kprove-vacuity.log; then
  printf '[expected WarnStuckClaimState missing]\n'
  status=1
elif ! rg -q 'implication check between the conditions has failed|cannot be rewritten further' \
    /audit-output/evidence/kprove-vacuity.log; then
  printf '[expected unmet-obligation diagnostic missing]\n'
  status=1
else
  printf '[expected semantic proof failure observed; non-vacuity condition satisfied]\n'
fi

printf 'FINAL_STATUS=%d\n' "$status"
exit "$status"
