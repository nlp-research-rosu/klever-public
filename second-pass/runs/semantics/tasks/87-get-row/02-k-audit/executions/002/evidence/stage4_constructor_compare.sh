#!/usr/bin/env bash
set -uo pipefail
set -x

python3 /audit-output/evidence/constructor_compare.py
rc=$?
printf 'constructor_level_compare_exit=%d\n' "$rc"
exit "$rc"
