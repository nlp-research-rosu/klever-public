#!/usr/bin/env bash
set +e
set -x

cd /tmp/audit-work/source || exit 90

cp audit-vacuity.k /audit-output/evidence/audit-vacuity.k
sha256sum audit-vacuity.k /audit-output/evidence/audit-vacuity.k

kprove audit-vacuity.k \
  --definition /tmp/audit-work/proof-kompiled \
  --spec-module AUDIT-VACUITY-SPEC \
  --dry-run \
  > /tmp/audit-work/runs/audit-vacuity-dry-run.out 2>&1
dry_run_exit=$?
printf 'fresh mutation dry-run/build exit: %s\n' "$dry_run_exit"
wc -lc /tmp/audit-work/runs/audit-vacuity-dry-run.out
sha256sum /tmp/audit-work/runs/audit-vacuity-dry-run.out
sed -n '1,40p' /tmp/audit-work/runs/audit-vacuity-dry-run.out
tail -n 40 /tmp/audit-work/runs/audit-vacuity-dry-run.out

kprove audit-vacuity.k \
  --definition /tmp/audit-work/proof-kompiled \
  --spec-module AUDIT-VACUITY-SPEC \
  2>&1 | tee /audit-output/evidence/stage6_vacuity_proof.raw.log
proof_exit=${PIPESTATUS[0]}
printf 'fresh false mutation proof exit: %s\n' "$proof_exit"

grep -nE 'WarnStuckClaimState|implication check|cannot be rewritten|#Top' \
  /audit-output/evidence/stage6_vacuity_proof.raw.log
residual_search_exit=$?
printf 'expected residual search exit: %s\n' "$residual_search_exit"

if [ "$dry_run_exit" -ne 0 ]; then
  exit 2
fi
if [ "$proof_exit" -eq 0 ]; then
  exit 3
fi
if [ "$residual_search_exit" -ne 0 ]; then
  exit 4
fi
exit 0
