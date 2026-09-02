#!/usr/bin/env bash
set -u

export PATH="/home/agent/.nix-profile/bin:$PATH"

echo '$ python3 /audit-output/evidence/stage4_witnesses.py'
python3 /audit-output/evidence/stage4_witnesses.py
witness_rc=$?
printf '[exit %d]\n\n' "$witness_rc"

echo '$ cp /audit-output/evidence/stage4_end_to_end.k /tmp/audit-work/stage4_end_to_end.k'
cp /audit-output/evidence/stage4_end_to_end.k /tmp/audit-work/stage4_end_to_end.k
copy_rc=$?
printf '[exit %d]\n\n' "$copy_rc"

echo '$ kprove stage4_end_to_end.k --definition verification-kompiled --spec-module AUDIT-END-TO-END'
(
  cd /tmp/audit-work || exit 1
  kprove stage4_end_to_end.k \
    --definition verification-kompiled \
    --spec-module AUDIT-END-TO-END
)
proof_rc=$?
printf '[exit %d]\n\n' "$proof_rc"

if (( witness_rc != 0 || copy_rc != 0 || proof_rc != 0 )); then
  exit 1
fi
