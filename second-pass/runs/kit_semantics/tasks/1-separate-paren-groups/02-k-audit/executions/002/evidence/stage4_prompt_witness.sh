#!/usr/bin/env bash
set -u

SCRATCH=/tmp/audit-work/reconstruction
LOG=/audit-output/evidence/stage4_witness_prompt_result_long.log
TEMPORARY="$(mktemp /tmp/audit-work/stage4_prompt_result.XXXXXX)"
COMMAND="cd '$SCRATCH' && timeout 180 kprove spec-witnesses.k --definition audit-verification-kompiled --spec-module SPEC-WITNESSES --claims SPEC-WITNESSES.prompt-result"

printf '$ %s\n' "$COMMAND" > "$LOG"
bash -o pipefail -c "$COMMAND" > "$TEMPORARY" 2>&1
status=$?
lines="$(wc -l < "$TEMPORARY")"
bytes="$(wc -c < "$TEMPORARY")"
printf '[captured output: %s lines, %s bytes]\n' "$lines" "$bytes" >> "$LOG"
if [ "$lines" -le 300 ]; then
  sed -n '1,300p' "$TEMPORARY" >> "$LOG"
else
  sed -n '1,60p' "$TEMPORARY" >> "$LOG"
  printf '[... bounded omission of middle output ...]\n' >> "$LOG"
  tail -n 240 "$TEMPORARY" >> "$LOG"
fi
printf '[exit %d]\n' "$status" >> "$LOG"
rm -f "$TEMPORARY"
printf 'stage4_witness_prompt_result_long exit=%d\\n' "$status"
exit "$status"
