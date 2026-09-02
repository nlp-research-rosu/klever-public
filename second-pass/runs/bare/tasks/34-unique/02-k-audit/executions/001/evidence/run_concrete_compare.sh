#!/usr/bin/env bash
set -uo pipefail
PS4='+ ${BASH_SOURCE##*/}:${LINENO}: '
set -x

python3 /audit-output/evidence/concrete_compare.py
status=$?
set +x
printf 'EXIT_STATUS=%s\n' "$status"
exit "$status"
