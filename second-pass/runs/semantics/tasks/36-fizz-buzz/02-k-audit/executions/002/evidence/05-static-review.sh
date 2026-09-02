#!/usr/bin/env bash
set -uo pipefail

LOG=/audit-output/evidence/05-static-review.log
: > "$LOG"

printf '%s\n' \
  '$ python3 /audit-output/evidence/build_rule_inventory.py > /audit-output/evidence/05-rule-inventory.md' \
  >> "$LOG"
python3 /audit-output/evidence/build_rule_inventory.py \
  > /audit-output/evidence/05-rule-inventory.md 2>> "$LOG"
command_status=$?
printf 'EXIT: %s\n\n' "$command_status" >> "$LOG"

run() {
  printf '$ %s\n' "$*" >> "$LOG"
  "$@" >> "$LOG" 2>&1
  command_status=$?
  printf 'EXIT: %s\n\n' "$command_status" >> "$LOG"
  return 0
}

run wc -l -c /audit-output/evidence/05-rule-inventory.md
run tail -8 /audit-output/evidence/05-rule-inventory.md
run rg -n -F \
  -e no-evaluators \
  -e 'symbol(' \
  -e 'priority(' \
  -e simplification \
  -e '[total' \
  -e '[function' \
  -e '[macro' \
  /tmp/audit-work/reviewer-002/scratch/reference-semantics \
  /tmp/audit-work/reviewer-002/scratch/verification.k
run rg -n -F \
  -e 'Module(' \
  -e FuncDef \
  -e 'Assign(' \
  -e 'Name(' \
  -e 'Int(' \
  -e 'While(' \
  -e 'Compare(' \
  -e CmpOp \
  -e BinOp \
  -e BoolOp \
  -e 'If(' \
  -e AugAssign \
  -e 'Return(' \
  -e 'Call(' \
  /tmp/audit-work/reviewer-002/scratch/solution.mpy
