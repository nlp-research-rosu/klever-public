#!/usr/bin/env bash
set -uo pipefail

definition=/tmp/audit-work/32-find-zero/verification-base-kompiled
spec=/tmp/audit-work/32-find-zero/spec.k
log_dir=/audit-output/evidence/stage3
failures=0

run_proof() {
  local label="$1"
  local module="$2"
  local claims="$3"
  local log="$log_dir/${label}.log"
  printf 'COMMAND: kprove %s --definition %s --spec-module %s --claims %s\n' \
    "$spec" "$definition" "$module" "$claims" > "$log"
  kprove "$spec" \
    --definition "$definition" \
    --spec-module "$module" \
    --claims "$claims" >> "$log" 2>&1
  local status=$?
  printf 'EXIT: %d\n' "$status" >> "$log"
  printf '%s exit=%d top_lines=%s\n' \
    "$label" "$status" "$(grep -c '^#Top$' "$log")"
  if (( status != 0 )) || ! grep -qx '#Top' "$log"; then
    failures=$((failures + 1))
  fi
}

run_proof \
  positive-1-find-prefixes \
  SPEC \
  SPEC.find-load,SPEC.find-init
run_proof \
  positive-2-poly-loops \
  SPEC-CONNECTION \
  SPEC-CONNECTION.poly-loop-empty,SPEC-CONNECTION.poly-loop-int,SPEC-CONNECTION.poly-loop-float
run_proof \
  positive-3-expand-loop \
  SPEC-CONNECTION \
  SPEC-CONNECTION.poly-loop-empty,SPEC-CONNECTION.poly-loop-int,SPEC-CONNECTION.poly-loop-float,SPEC-CONNECTION.expand-loop
run_proof \
  positive-4-bisect-head \
  SPEC-CONNECTION \
  SPEC-CONNECTION.bisect-head
run_proof \
  positive-5-bisect-loop \
  SPEC-CONNECTION \
  SPEC-CONNECTION.poly-loop-empty,SPEC-CONNECTION.poly-loop-int,SPEC-CONNECTION.poly-loop-float,SPEC-CONNECTION.bisect-loop

printf 'positive_proof_failures=%d\n' "$failures"
exit "$failures"
