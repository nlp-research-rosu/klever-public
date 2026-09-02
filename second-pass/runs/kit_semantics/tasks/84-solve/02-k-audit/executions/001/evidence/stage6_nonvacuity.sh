#!/usr/bin/env bash
set -euo pipefail

work=/tmp/audit-work/84-solve
evidence=/audit-output/evidence
raw=/tmp/audit-work/84-solve/raw-logs
cd "$work"
cp "$evidence/fresh-false-spec.k" .

dry_log="$evidence/stage6-false-dry-run.log"
dry_raw="$raw/stage6-false-dry-run.raw.log"
printf '%s\n' \
  'COMMAND: kprove fresh-false-spec.k --definition verification-audit-kompiled --spec-module FRESH-FALSE-SPEC --dry-run' \
  > "$dry_log"
set +e
kprove fresh-false-spec.k \
  --definition verification-audit-kompiled \
  --spec-module FRESH-FALSE-SPEC \
  --dry-run \
  > "$dry_raw" 2>&1
dry_status=$?
set -e
{
  printf 'EXIT_STATUS=%s\n' "$dry_status"
  printf 'OUTPUT_LINES=%s\n' "$(wc -l < "$dry_raw")"
  sed -n '1,160p' "$dry_raw"
} >> "$dry_log"
if [[ $dry_status -ne 0 ]]; then
  exit "$dry_status"
fi

proof_log="$evidence/stage6-false-proof.log"
proof_raw="$raw/stage6-false-proof.raw.log"
printf '%s\n' \
  'COMMAND: kprove fresh-false-spec.k --definition verification-audit-kompiled --spec-module FRESH-FALSE-SPEC' \
  > "$proof_log"
set +e
kprove fresh-false-spec.k \
  --definition verification-audit-kompiled \
  --spec-module FRESH-FALSE-SPEC \
  > "$proof_raw" 2>&1
proof_status=$?
set -e
{
  printf 'EXIT_STATUS=%s\n' "$proof_status"
  printf 'OUTPUT_LINES=%s\n' "$(wc -l < "$proof_raw")"
  sed -n '1,200p' "$proof_raw"
  if [[ $(wc -l < "$proof_raw") -gt 400 ]]; then
    printf '[... bounded log: middle omitted ...]\n'
    tail -n 200 "$proof_raw"
  else
    sed -n '201,400p' "$proof_raw"
  fi
} >> "$proof_log"
if [[ $proof_status -eq 0 ]]; then
  printf 'ERROR: false ground result unexpectedly proved\n' >&2
  exit 1
fi
rg -q 'WarnStuckClaimState' "$proof_raw"
printf 'EXPECTED_FALSE_OBLIGATION_FAILURE=%s\n' "$proof_status"
