#!/usr/bin/env bash
set -uo pipefail

definition=/tmp/audit-work/130-tri-audit/runtime-audit-kompiled
program=/audit-output/evidence/runtime_checks.mpy
log=/audit-output/evidence/stage3_concrete_retry.full.log

printf 'COMMAND: krun %q --definition %q --output none\n' "$program" "$definition"
krun "$program" --definition "$definition" --output none >"$log" 2>&1
status=$?
printf 'EXIT_STATUS: %d\n' "$status"
printf '%s\n' 'OUTPUT_BEGIN'
sed -n '1,200p' "$log"
printf '%s\n' 'OUTPUT_END'
exit "$status"
