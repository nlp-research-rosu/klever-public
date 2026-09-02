#!/usr/bin/env bash
set -uo pipefail

audit_work=/tmp/audit-work/130-tri-audit
source_spec=/audit-output/evidence/spec-vacuity-audit.k
definition="$audit_work/verification-proof-kompiled"
cd "$audit_work" || exit 2

printf 'SATISFYING_WITNESS: N=3, and 3 >= 0\n'
printf 'FALSE_OBLIGATION: expected last element 9 instead of actual 8\n'

printf 'COMMAND: cp -p %s %s/spec-vacuity-audit.k\n' \
  "$source_spec" "$audit_work"
cp -p "$source_spec" "$audit_work/spec-vacuity-audit.k"
copy_status=$?
printf 'COPY_EXIT_STATUS=%s\n' "$copy_status"

printf 'COMMAND: kprove spec-vacuity-audit.k --dry-run\n'
kprove spec-vacuity-audit.k \
  --definition "$definition" \
  --spec-module SPEC-VACUITY-AUDIT \
  --dry-run
dry_run_status=$?
printf 'MUTATION_BUILD_EXIT_STATUS=%s\n' "$dry_run_status"
if [[ "$dry_run_status" -ne 0 ]]; then
  exit "$dry_run_status"
fi

printf 'COMMAND: kprove spec-vacuity-audit.k (expected unmet obligation)\n'
kprove spec-vacuity-audit.k \
  --definition "$definition" \
  --spec-module SPEC-VACUITY-AUDIT
prove_status=$?
printf 'EXPECTED_FALSE_POSTCONDITION_PROOF_EXIT_STATUS=%s\n' "$prove_status"

if [[ "$copy_status" -ne 0 ]]; then
  exit 1
fi
if [[ "$prove_status" -eq 0 ]]; then
  printf 'ERROR: false result mutation unexpectedly closed\n' >&2
  exit 1
fi

printf 'NON_VACUITY_PASS\n'
