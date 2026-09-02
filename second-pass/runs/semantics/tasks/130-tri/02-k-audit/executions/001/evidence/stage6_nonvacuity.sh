#!/usr/bin/env bash
set -u

work_dir=/tmp/audit-work/reconstruction
cd "$work_dir" || exit 90

echo '$ test ! -e /candidate/spec-vacuity.k'
test ! -e /candidate/spec-vacuity.k
echo "exit=$?"

echo '$ cp /audit-output/evidence/spec-vacuity-audit.k /tmp/audit-work/reconstruction/spec-vacuity-audit.k'
cp /audit-output/evidence/spec-vacuity-audit.k \
  /tmp/audit-work/reconstruction/spec-vacuity-audit.k
copy_rc=$?
echo "exit=$copy_rc"

echo '$ kprove spec-vacuity-audit.k --definition verification-kompiled --spec-module TRI-VACUITY-AUDIT-SPEC --dry-run'
kprove spec-vacuity-audit.k \
  --definition verification-kompiled \
  --spec-module TRI-VACUITY-AUDIT-SPEC \
  --dry-run
dry_rc=$?
echo "exit=$dry_rc"

echo '$ kprove spec-vacuity-audit.k --definition verification-kompiled --spec-module TRI-VACUITY-AUDIT-SPEC --output pretty'
kprove spec-vacuity-audit.k \
  --definition verification-kompiled \
  --spec-module TRI-VACUITY-AUDIT-SPEC \
  --output pretty
proof_rc=$?
echo "exit=$proof_rc"
echo "SUMMARY copy=$copy_rc dry_run=$dry_rc mutated_proof=$proof_rc expected_mutated_proof=nonzero"

if [ "$copy_rc" -ne 0 ] || [ "$dry_rc" -ne 0 ]; then
  exit 1
fi
if [ "$proof_rc" -eq 0 ]; then
  exit 2
fi
exit 0
