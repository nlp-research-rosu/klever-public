#!/usr/bin/env bash
set -uo pipefail

spec=/audit-output/evidence/spec-vacuity-audit.k
definition=/tmp/audit-work/candidate/proof-kompiled

echo "WITNESS: input \"abcdef\" satisfies the unconditional entry domain; candidate Python and rebuilt K both return 3, so VInt(4) is false."
echo "COMMAND: kprove $spec --definition $definition --spec-module AUDIT-SPEC-VACUITY --dry-run"
kprove "$spec" \
  --definition "$definition" \
  --spec-module AUDIT-SPEC-VACUITY \
  --dry-run
dry_status=$?
echo "EXIT_STATUS: $dry_status"
if (( dry_status != 0 )); then
  exit "$dry_status"
fi

echo "COMMAND: kprove $spec --definition $definition --spec-module AUDIT-SPEC-VACUITY"
kprove "$spec" \
  --definition "$definition" \
  --spec-module AUDIT-SPEC-VACUITY
proof_status=$?
echo "EXIT_STATUS: $proof_status (nonzero expected)"
if (( proof_status == 0 )); then
  exit 1
fi
exit 0
