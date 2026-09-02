#!/usr/bin/env bash
set -uo pipefail

WORK=/tmp/audit-work/124-valid-date
EVIDENCE=/audit-output/evidence
export PATH="/root/.nix-profile/bin:$PATH"

run_bounded() {
  local label=$1
  shift
  local raw="$WORK/${label}.raw.log"
  local log="$EVIDENCE/${label}.log"
  {
    printf 'WORKDIR: %s\n' "$WORK"
    printf 'COMMAND:'
    printf ' %q' "$@"
    printf '\n'
  } >"$log"
  (
    cd "$WORK"
    "$@"
  ) >"$raw" 2>&1
  local status=$?
  {
    printf '%s\n' 'OUTPUT_HEAD:'
    sed -n '1,100p' "$raw"
    printf '%s\n' 'OUTPUT_TAIL:'
    tail -n 180 "$raw"
    printf 'EXIT_STATUS: %s\n' "$status"
  } >>"$log"
  printf '%s exit=%s\n' "$label" "$status"
  tail -n 35 "$log"
  return "$status"
}

run_bounded 06a_mutation_dry_run \
  kprove spec-vacuity-audit.k \
  --definition audit-verification-kompiled \
  --spec-module AUDIT-SPEC-VACUITY \
  --dry-run
DRY_STATUS=$?

run_bounded 06b_mutation_proof \
  kprove spec-vacuity-audit.k \
  --definition audit-verification-kompiled \
  --spec-module AUDIT-SPEC-VACUITY
PROOF_STATUS=$?

WARN_COUNT=$(rg -c 'WarnStuckClaimState' "$WORK/06b_mutation_proof.raw.log" || true)
TOP_COUNT=$(rg -c '^#Top$' "$WORK/06b_mutation_proof.raw.log" || true)
TRUE_FALSE_COUNT=$(rg -c 'true|false|Bool' "$WORK/06b_mutation_proof.raw.log" || true)
WARN_COUNT=${WARN_COUNT:-0}
TOP_COUNT=${TOP_COUNT:-0}
TRUE_FALSE_COUNT=${TRUE_FALSE_COUNT:-0}

SUMMARY="$EVIDENCE/06_mutation_summary.log"
{
  printf 'witness=%q\n' '02-29-2000'
  printf 'expected_program_result=true\n'
  printf 'mutated_required_result=false\n'
  printf 'dry_run_status=%s\n' "$DRY_STATUS"
  printf 'proof_status=%s\n' "$PROOF_STATUS"
  printf 'stuck_warning_count=%s\n' "$WARN_COUNT"
  printf 'top_count=%s\n' "$TOP_COUNT"
  printf 'result_term_mentions=%s\n' "$TRUE_FALSE_COUNT"
  if [ "$DRY_STATUS" -eq 0 ] &&
     [ "$PROOF_STATUS" -ne 0 ] &&
     [ "$WARN_COUNT" -gt 0 ] &&
     [ "$TOP_COUNT" -eq 0 ]; then
    printf 'NON_VACUITY=PASS\n'
  else
    printf 'NON_VACUITY=FAIL\n'
  fi
} >"$SUMMARY"
sed -n '1,160p' "$SUMMARY"

if [ "$DRY_STATUS" -ne 0 ] ||
   [ "$PROOF_STATUS" -eq 0 ] ||
   [ "$WARN_COUNT" -eq 0 ] ||
   [ "$TOP_COUNT" -ne 0 ]; then
  exit 1
fi
