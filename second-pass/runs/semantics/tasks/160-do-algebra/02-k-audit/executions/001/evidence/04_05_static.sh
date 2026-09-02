#!/usr/bin/env bash
set -u

LOG=/audit-output/evidence/04_05_static.log
: > "$LOG"

run() {
  printf 'COMMAND: ' >> "$LOG"
  printf '%q ' "$@" >> "$LOG"
  printf '\n' >> "$LOG"
  "$@" >> "$LOG" 2>&1
  status=$?
  printf 'EXIT: %d\n\n' "$status" >> "$LOG"
  return 0
}

run python3 /audit-output/evidence/04_claim_witnesses.py
run python3 /audit-output/evidence/05_rule_inventory.py
run wc -l /audit-output/evidence/05_rule_inventory.txt
run sha256sum \
  /audit-output/evidence/04_claim_witnesses.json \
  /audit-output/evidence/05_rule_inventory.json \
  /audit-output/evidence/05_rule_inventory.txt
