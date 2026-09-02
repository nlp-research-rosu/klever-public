#!/usr/bin/env bash
set -u

WORK=/tmp/audit-work/proof-audit.Dl0nBZ/candidate
export PATH="/home/agent/.nix-profile/bin:$PATH"

printf '$ python3 /audit-output/evidence/06-adequacy-witness.py\n'
python3 /audit-output/evidence/06-adequacy-witness.py
witness_status=$?
printf '[exit %d]\n' "$witness_status"

cd "$WORK" || exit 90
printf '\n$ kprove /audit-output/evidence/program-pinning.k'
printf ' --definition verification-kompiled'
printf ' --spec-module PROGRAM-PINNING -I .\n'
kprove /audit-output/evidence/program-pinning.k \
  --definition verification-kompiled \
  --spec-module PROGRAM-PINNING \
  -I .
pin_status=$?
printf '[exit %d]\n' "$pin_status"

if test "$witness_status" -eq 0 && test "$pin_status" -eq 0; then
  exit 0
fi
exit 1
