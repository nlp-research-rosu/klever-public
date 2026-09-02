#!/usr/bin/env bash
set -uo pipefail

work=/tmp/audit-work/prime-fib-audit
evidence=/audit-output/evidence
summary="$evidence/kprove-positive-summary.log"
: > "$summary"

run_claim() {
  local n=$1
  local label="PRIME-FIB-SPEC.pf${n}"
  local log="$evidence/kprove-pf${n}.log"
  printf 'COMMAND: timeout 1200s kprove spec.k --definition proof-kompiled --spec-module PRIME-FIB-SPEC --claims %s\n' "$label" > "$log"
  (
    cd "$work" || exit 125
    timeout 1200s kprove spec.k \
      --definition proof-kompiled \
      --spec-module PRIME-FIB-SPEC \
      --claims "$label"
  ) >> "$log" 2>&1
  local status=$?
  printf 'EXIT: %s\n' "$status" >> "$log"
  local tops
  tops=$(grep -c -x '#Top' "$log" || true)
  printf 'CLAIM pf%s EXIT=%s TOP_LINES=%s\n' "$n" "$status" "$tops" >> "$summary"
  if [[ "$status" -ne 0 || "$tops" -lt 1 ]]; then
    return 1
  fi
}

overall=0
for batch in "11 10 9" "8 7 6" "5 4 3" "2 1"; do
  pids=()
  ns=()
  for n in $batch; do
    run_claim "$n" &
    pids+=("$!")
    ns+=("$n")
  done
  for i in "${!pids[@]}"; do
    if ! wait "${pids[$i]}"; then
      printf 'FAILED pf%s\n' "${ns[$i]}" >> "$summary"
      overall=1
    fi
  done
done

printf 'OVERALL EXIT: %s\n' "$overall" >> "$summary"
cat "$summary"
exit "$overall"
