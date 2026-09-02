#!/usr/bin/env bash
set -uo pipefail

work=/tmp/audit-work/proof
evidence=/audit-output/evidence
summary="$evidence/08-positive-claims-summary.log"
failed=0
count=0

: > "$summary"
while IFS= read -r label; do
  count=$((count + 1))
  log="$evidence/08-claim-${label}.log"
  command=(
    kprove spec.k
    --definition fresh-verification-kompiled
    --spec-module SPEC
    --claims "SPEC.$label"
  )
  printf 'COMMAND:' | tee "$log"
  printf ' %q' "${command[@]}" | tee -a "$log"
  printf '\n' | tee -a "$log"
  (
    cd "$work" || exit 125
    "${command[@]}"
  ) 2>&1 | tee -a "$log"
  status=${PIPESTATUS[0]}
  top_count=$(awk '$0 == "#Top" { count += 1 } END { print count + 0 }' "$log")
  printf 'CLAIM=%s EXIT_STATUS=%s TOP_LINES=%s\n' \
    "$label" "$status" "$top_count" | tee -a "$log" "$summary"
  if [[ "$status" -ne 0 || "$top_count" -lt 1 ]]; then
    failed=$((failed + 1))
  fi
done < <(sed -n 's/^  claim \[\([^]]*\)\]:$/\1/p' "$work/spec.k")

printf 'TOTAL_CLAIMS=%s\nFAILED_CLAIMS=%s\n' "$count" "$failed" | tee -a "$summary"
if [[ "$failed" -ne 0 || "$count" -eq 0 ]]; then
  exit 1
fi
