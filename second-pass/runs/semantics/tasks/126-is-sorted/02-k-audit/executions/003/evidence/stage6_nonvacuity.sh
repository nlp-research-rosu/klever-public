#!/usr/bin/env bash
set -u
set -o pipefail

WORK=/tmp/audit-work/126-is-sorted-audit-003
EVIDENCE=/audit-output/evidence
cd "$WORK" || exit 98

run_logged() {
  local label=$1
  shift
  local log="$EVIDENCE/$label.log"
  {
    printf '$'
    printf ' %q' "$@"
    printf '\n'
  } | tee "$log"
  timeout 120 "$@" 2>&1 | tee -a "$log"
  local command_status=${PIPESTATUS[0]}
  printf 'exit=%s\n' "$command_status" | tee -a "$log"
  return "$command_status"
}

run_logged stage6_mutation_dry_run \
  kprove spec-vacuity-audit.k \
    --definition audit-verification-kompiled \
    --spec-module IS-SORTED-VACUITY-AUDIT \
    --dry-run \
    --output pretty
dry_status=$?

run_logged stage6_mutation_proof \
  kprove spec-vacuity-audit.k \
    --definition audit-verification-kompiled \
    --spec-module IS-SORTED-VACUITY-AUDIT \
    --output pretty
proof_status=$?

printf 'expected dry_run=0 actual=%s; expected proof_nonzero actual=%s\n' \
  "$dry_status" "$proof_status" \
  | tee "$EVIDENCE/stage6_nonvacuity_summary.log"

if [[ "$dry_status" -eq 0 && "$proof_status" -ne 0 && "$proof_status" -ne 124 ]]; then
  exit 0
fi
exit 1
