#!/usr/bin/env bash
set -u

SCRATCH=/tmp/audit-work/reconstruction
LOG=/audit-output/evidence/stage3_explicit_claims.log
TEMPORARY="$(mktemp /tmp/audit-work/stage3_explicit_claims.XXXXXX)"
COMMAND="cd '$SCRATCH' && timeout 300 kprove spec.k --definition audit-verification-kompiled --spec-module SPEC --claims SPEC.loop-invariant,SPEC.function-correct"

printf '$ %s\n' "$COMMAND" > "$LOG"
bash -o pipefail -c "$COMMAND" > "$TEMPORARY" 2>&1
status=$?
lines="$(wc -l < "$TEMPORARY")"
bytes="$(wc -c < "$TEMPORARY")"
printf '[captured output: %s lines, %s bytes]\n' "$lines" "$bytes" >> "$LOG"
if [ "$lines" -le 500 ]; then
  sed -n '1,500p' "$TEMPORARY" >> "$LOG"
else
  sed -n '1,80p' "$TEMPORARY" >> "$LOG"
  printf '[... bounded omission of middle output ...]\n' >> "$LOG"
  tail -n 420 "$TEMPORARY" >> "$LOG"
fi
printf '[exit %d]\n' "$status" >> "$LOG"
rm -f "$TEMPORARY"
printf 'stage3_explicit_claims exit=%d\n' "$status"
exit "$status"
