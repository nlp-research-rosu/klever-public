#!/usr/bin/env bash
set -u

SCRATCH=/tmp/audit-work/reconstruction
EVIDENCE=/audit-output/evidence
overall=0

capture() {
  local label="$1"
  local command_text="$2"
  local temporary
  temporary="$(mktemp /tmp/audit-work/${label}.XXXXXX)"
  printf '$ %s\n' "$command_text" > "$EVIDENCE/${label}.log"
  bash -o pipefail -c "$command_text" > "$temporary" 2>&1
  local status=$?
  local lines
  lines="$(wc -l < "$temporary")"
  local bytes
  bytes="$(wc -c < "$temporary")"
  printf '[captured output: %s lines, %s bytes]\n' "$lines" "$bytes" >> "$EVIDENCE/${label}.log"
  if [ "$lines" -le 500 ]; then
    sed -n '1,500p' "$temporary" >> "$EVIDENCE/${label}.log"
  else
    sed -n '1,80p' "$temporary" >> "$EVIDENCE/${label}.log"
    printf '[... bounded omission of middle output ...]\n' >> "$EVIDENCE/${label}.log"
    tail -n 420 "$temporary" >> "$EVIDENCE/${label}.log"
  fi
  printf '[exit %d]\n' "$status" >> "$EVIDENCE/${label}.log"
  rm -f "$temporary"
  CAPTURE_STATUS="$status"
  printf '%s exit=%d\n' "$label" "$status"
}

capture stage6_copy_mutation \
  "cp '$EVIDENCE/spec-audit-false.k' '$SCRATCH/spec-audit-false.k'"
if [ "$CAPTURE_STATUS" -ne 0 ]; then
  overall=1
fi

capture stage6_false_dry_run \
  "cd '$SCRATCH' && kprove spec-audit-false.k --definition audit-verification-kompiled --spec-module SPEC-AUDIT-FALSE --dry-run"
if [ "$CAPTURE_STATUS" -ne 0 ]; then
  overall=1
fi

capture stage6_false_proof \
  "cd '$SCRATCH' && timeout 120 kprove spec-audit-false.k --definition audit-verification-kompiled --spec-module SPEC-AUDIT-FALSE"
if [ "$CAPTURE_STATUS" -eq 0 ] || [ "$CAPTURE_STATUS" -eq 124 ]; then
  overall=1
fi

if ! rg -q 'WarnStuckClaimState' "$EVIDENCE/stage6_false_proof.log"; then
  overall=1
fi
if ! rg -Fq 'iCons ( 40' "$EVIDENCE/stage6_false_proof.log"; then
  overall=1
fi

printf 'NONVACUITY_EXPECTATIONS_MET=%s\n' "$([ "$overall" -eq 0 ] && echo true || echo false)"
exit "$overall"
