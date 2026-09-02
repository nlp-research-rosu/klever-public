#!/usr/bin/env bash
set -u

WORK=/tmp/audit-work/proof-audit.Dl0nBZ/candidate
SPEC=/audit-output/evidence/spec-vacuity-audit.k
export PATH="/home/agent/.nix-profile/bin:$PATH"

cd "$WORK" || exit 90

printf '$ python3 /audit-output/evidence/04-vacuity-witness.py\n'
python3 /audit-output/evidence/04-vacuity-witness.py
witness_status=$?
printf '[exit %d]\n' "$witness_status"

printf '\n$ kprove %s --definition verification-kompiled' "$SPEC"
printf ' --spec-module SPEC-VACUITY-AUDIT -I . --dry-run\n'
kprove "$SPEC" \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY-AUDIT \
  -I . \
  --dry-run
dry_status=$?
printf '[exit %d]\n' "$dry_status"

printf '\n$ kprove %s --definition verification-kompiled' "$SPEC"
printf ' --spec-module SPEC-VACUITY-AUDIT -I .\n'
kprove "$SPEC" \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY-AUDIT \
  -I .
proof_status=$?
printf '[exit %d]\n' "$proof_status"

if test "$witness_status" -eq 0 &&
   test "$dry_status" -eq 0 &&
   test "$proof_status" -ne 0; then
  printf 'EXPECTED_NON_VACUITY_REJECTION\n'
  exit 0
fi

printf 'NON_VACUITY_TEST_INVALID\n'
exit 1
