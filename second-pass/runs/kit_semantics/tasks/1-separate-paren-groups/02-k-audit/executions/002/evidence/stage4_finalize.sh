#!/usr/bin/env bash
set -u

SCRATCH=/tmp/audit-work/reconstruction
EVIDENCE=/audit-output/evidence
overall=0

run_bounded() {
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
  if [ "$lines" -le 300 ]; then
    sed -n '1,300p' "$temporary" >> "$EVIDENCE/${label}.log"
  else
    sed -n '1,60p' "$temporary" >> "$EVIDENCE/${label}.log"
    printf '[... bounded omission of middle output ...]\n' >> "$EVIDENCE/${label}.log"
    tail -n 240 "$temporary" >> "$EVIDENCE/${label}.log"
  fi
  printf '[exit %d]\n' "$status" >> "$EVIDENCE/${label}.log"
  rm -f "$temporary"
  printf '%s exit=%d\n' "$label" "$status"
  if [ "$status" -ne 0 ]; then
    overall=1
  fi
}

run_bounded stage4_pinning \
  "python3 '$EVIDENCE/pinning_check.py'"

for claim in empty-valid empty-result single-valid single-result prompt-valid prompt-result; do
  label="stage4_witness_${claim//-/_}"
  run_bounded "$label" \
    "cd '$SCRATCH' && timeout 30 kprove spec-witnesses.k --definition audit-verification-kompiled --spec-module SPEC-WITNESSES --claims SPEC-WITNESSES.$claim"
done

exit "$overall"
