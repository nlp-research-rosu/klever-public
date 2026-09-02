#!/usr/bin/env bash
set -uo pipefail

audit_work=/tmp/audit-work/audit79
status=0

echo "COMMAND: rg -n syntax|configuration|rule|claim semantic.k verification.k spec.k"
rg -n '^[[:space:]]*(syntax|configuration|rule|claim)([[:space:]]|$)' \
  "$audit_work/semantic.k" "$audit_work/verification.k" "$audit_work/spec.k"
command_status=$?
echo "EXIT_STATUS $command_status"
if (( command_status != 0 )); then status=1; fi

echo "COMMAND: rg -n total|functional|simplification|concrete|priority|owise|macro|alias|opaque semantic.k verification.k spec.k"
rg -n '\[(total|functional|simplification|concrete|priority|owise|macro|alias|opaque)(,|\])|priority|opaque' \
  "$audit_work/semantic.k" "$audit_work/verification.k" "$audit_work/spec.k"
command_status=$?
echo "EXIT_STATUS $command_status (expected 1: no such declarations)"
if (( command_status != 1 )); then status=1; fi

echo "COMMAND: rg -o constructor names used by solution.mpy"
rg -o 'Module|FuncDef|Params|Return|BinOp|Str|Subscript|Call|Name|Slice|Int|NoBound' \
  "$audit_work/solution.mpy" | sort | uniq -c
command_status=$?
echo "EXIT_STATUS $command_status"
if (( command_status != 0 )); then status=1; fi

echo "SCRIPT_EXIT_STATUS $status"
exit "$status"
