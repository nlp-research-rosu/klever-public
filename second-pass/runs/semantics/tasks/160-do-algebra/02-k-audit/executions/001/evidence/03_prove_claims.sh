#!/usr/bin/env bash
set -u

WORK=/tmp/audit-work/rebuild
LOG=/audit-output/evidence/03_positive_claims.log
: > "$LOG"

labels=(
  plus
  minus
  times
  floor
  power
  minus-assoc
  floor-assoc
  power-assoc
  prompt-precedence
  mixed-precedence
)

cd "$WORK" || exit 1
overall=0

for label in "${labels[@]}"; do
  raw="/audit-output/evidence/03_claim_${label}.log"
  printf 'COMMAND: kprove spec.k --definition verification-audit-kompiled --spec-module SPEC --claims %s\n' "$label" | tee -a "$LOG" > "$raw"
  kprove spec.k \
    --definition verification-audit-kompiled \
    --spec-module SPEC \
    --claims "$label" \
    >> "$raw" 2>&1
  status=$?
  top=no
  if grep -Fxq '#Top' "$raw"; then
    top=yes
  fi
  printf 'EXIT: %d\nHAS_EXACT_TOP: %s\n\n' "$status" "$top" | tee -a "$LOG" >> "$raw"
  printf '%s exit=%d exact_top=%s\n' "$label" "$status" "$top" >> "$LOG"
  if [ "$status" -ne 0 ] || [ "$top" != yes ]; then
    overall=1
  fi
done

printf 'OVERALL_EXIT: %d\n' "$overall" >> "$LOG"
exit "$overall"
