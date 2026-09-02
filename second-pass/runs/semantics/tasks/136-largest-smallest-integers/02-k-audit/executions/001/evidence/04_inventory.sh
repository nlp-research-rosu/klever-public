#!/usr/bin/env bash
set -u

printf 'COMMAND: bash /audit-output/evidence/04_inventory.sh\n'
printf 'RUN: python3 /audit-output/evidence/rule_inventory.py\n'
python3 /audit-output/evidence/rule_inventory.py
inventory_status=$?
printf 'EXIT rule inventory: %d\n' "$inventory_status"

printf 'RUN: rg used source constructors in solution.mpy\n'
rg -n 'Module|FuncDef|Params|Assign|Name|Int|For|If|Compare|CmpOp|BoolOp|Return|TupleExpr|NoneVal' \
  /tmp/audit-work/reconstruction/solution.mpy
constructors_status=$?
printf 'EXIT used-constructor search: %d\n' "$constructors_status"

if [[ "$inventory_status" -ne 0 || "$constructors_status" -ne 0 ]]; then
  exit 1
fi
printf 'FINAL EXIT: 0\n'
