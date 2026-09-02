#!/usr/bin/env bash
set -uo pipefail
PS4='+ ${BASH_SOURCE##*/}:${LINENO}: '
set -x

python3 /audit-output/evidence/differential_test.py \
  /tmp/audit-work/34-unique/reference/canonical.py \
  /tmp/audit-work/34-unique/candidate-source/solution.py
status=$?
set +x
printf 'EXIT_STATUS=%s\n' "$status"
exit "$status"
