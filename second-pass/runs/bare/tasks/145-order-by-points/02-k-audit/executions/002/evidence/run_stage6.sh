#!/usr/bin/env bash
set -u
set -x

cd /tmp/audit-work/reconstruction || exit 90
cp /audit-output/evidence/spec-vacuity-audit.k .
copy_rc=$?

kprove spec-vacuity-audit.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY-AUDIT \
  --dry-run
dry_run_rc=$?

kprove spec-vacuity-audit.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY-AUDIT
false_proof_rc=$?

python3 -c 'import solution; x=[1,11,-1,-11,-12]; print(f"satisfying_input={x!r} actual={solution.order_by_points(x)!r} deliberately_claimed=[-1,-11,1,-12,12]")'
witness_rc=$?

set +x
printf 'copy_exit=%d\n' "$copy_rc"
printf 'dry_run_exit=%d\n' "$dry_run_rc"
printf 'false_proof_exit=%d expected_nonzero=1\n' "$false_proof_rc"
printf 'witness_exit=%d\n' "$witness_rc"
test "$copy_rc" -eq 0 \
  && test "$dry_run_rc" -eq 0 \
  && test "$false_proof_rc" -ne 0 \
  && test "$witness_rc" -eq 0
