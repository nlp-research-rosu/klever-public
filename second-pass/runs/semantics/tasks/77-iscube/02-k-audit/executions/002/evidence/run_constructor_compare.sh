#!/usr/bin/env bash
set -uo pipefail

command=(python3 /audit-output/evidence/constructor_compare.py)
printf 'COMMAND:'
printf ' %q' "${command[@]}"
printf '\n'
"${command[@]}"
status=$?
printf 'EXIT_STATUS: %s\n' "$status"
exit "$status"
