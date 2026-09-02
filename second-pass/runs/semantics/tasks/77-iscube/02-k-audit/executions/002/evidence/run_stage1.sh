#!/usr/bin/env bash
set -uo pipefail

log=/audit-output/evidence/stage1_integrity.log
command=(python3 /audit-output/evidence/stage1_integrity.py)
printf 'COMMAND:'
printf ' %q' "${command[@]}"
printf '\n'
"${command[@]}"
status=$?
printf 'EXIT_STATUS: %s\n' "$status"
exit "$status"
