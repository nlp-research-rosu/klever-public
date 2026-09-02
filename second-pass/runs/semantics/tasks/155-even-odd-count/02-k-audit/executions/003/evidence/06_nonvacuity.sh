#!/usr/bin/env bash
set -u

kpath="/home/agent/.nix-profile/bin:$PATH"

printf '$ kprove /audit-output/evidence/06_spec_vacuity.k --definition /tmp/audit-work/fresh/verification-kompiled --spec-module AUDIT-SPEC-VACUITY --dry-run\n'
env PATH="$kpath" kprove /audit-output/evidence/06_spec_vacuity.k \
  --definition /tmp/audit-work/fresh/verification-kompiled \
  --spec-module AUDIT-SPEC-VACUITY \
  --dry-run
status=$?
printf '[exit %d; expected zero]\n' "$status"
test "$status" -eq 0 || exit "$status"

printf '$ kprove /audit-output/evidence/06_spec_vacuity.k --definition /tmp/audit-work/fresh/verification-kompiled --spec-module AUDIT-SPEC-VACUITY\n'
env PATH="$kpath" kprove /audit-output/evidence/06_spec_vacuity.k \
  --definition /tmp/audit-work/fresh/verification-kompiled \
  --spec-module AUDIT-SPEC-VACUITY
status=$?
printf '[exit %d; expected nonzero]\n' "$status"
test "$status" -ne 0
