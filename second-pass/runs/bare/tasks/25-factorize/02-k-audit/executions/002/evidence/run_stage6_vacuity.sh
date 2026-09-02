#!/usr/bin/env bash
set -uo pipefail

printf '$ kprove /audit-output/evidence/fresh-vacuity-spec.k -I /tmp/audit-work/25-factorize --definition fresh-verification-kompiled --spec-module FRESH-VACUITY-SPEC --dry-run\n'
kprove /audit-output/evidence/fresh-vacuity-spec.k \
  -I /tmp/audit-work/25-factorize \
  --definition fresh-verification-kompiled \
  --spec-module FRESH-VACUITY-SPEC \
  --dry-run
dry_run_status=$?
printf 'EXIT STATUS: %d\n' "$dry_run_status"

printf '$ kprove /audit-output/evidence/fresh-vacuity-spec.k -I /tmp/audit-work/25-factorize --definition fresh-verification-kompiled --spec-module FRESH-VACUITY-SPEC\n'
kprove /audit-output/evidence/fresh-vacuity-spec.k \
  -I /tmp/audit-work/25-factorize \
  --definition fresh-verification-kompiled \
  --spec-module FRESH-VACUITY-SPEC
proof_status=$?
printf 'EXIT STATUS: %d\n' "$proof_status"

printf 'MUTATION_BUILD_STATUS=%d\n' "$dry_run_status"
printf 'MUTATION_PROOF_STATUS=%d (expected nonzero)\n' "$proof_status"

if (( dry_run_status != 0 )); then
  exit 1
fi
if (( proof_status == 0 )); then
  exit 1
fi
exit 0
