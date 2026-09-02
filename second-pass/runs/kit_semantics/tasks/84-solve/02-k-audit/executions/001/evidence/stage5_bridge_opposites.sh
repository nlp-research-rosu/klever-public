#!/usr/bin/env bash
set -euo pipefail

work=/tmp/audit-work/84-solve
evidence=/audit-output/evidence
raw=/tmp/audit-work/84-solve/raw-logs
cd "$work"
cp "$evidence/fresh-bridge-negative.k" .

for claim in wrong-mod wrong-floordiv; do
  log="$evidence/stage5-bridge-opposite-$claim.log"
  raw_log="$raw/stage5-bridge-opposite-$claim.raw.log"
  printf 'COMMAND: kprove fresh-bridge-negative.k --definition bridge-audit-kompiled --spec-module FRESH-BRIDGE-NEGATIVE --claims FRESH-BRIDGE-NEGATIVE.%s\n' \
    "$claim" > "$log"
  set +e
  kprove fresh-bridge-negative.k \
    --definition bridge-audit-kompiled \
    --spec-module FRESH-BRIDGE-NEGATIVE \
    --claims "FRESH-BRIDGE-NEGATIVE.$claim" \
    > "$raw_log" 2>&1
  status=$?
  set -e
  {
    printf 'EXIT_STATUS=%s\n' "$status"
    printf 'OUTPUT_LINES=%s\n' "$(wc -l < "$raw_log")"
    sed -n '1,200p' "$raw_log"
  } >> "$log"
  if [[ $status -eq 0 ]]; then
    printf 'ERROR: opposite arithmetic value unexpectedly proved: %s\n' "$claim" >&2
    exit 1
  fi
  rg -q 'WarnStuckClaimState' "$raw_log"
done
