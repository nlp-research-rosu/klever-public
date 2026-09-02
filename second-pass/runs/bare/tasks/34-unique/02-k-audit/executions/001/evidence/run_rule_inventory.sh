#!/usr/bin/env bash
set -uo pipefail
PS4='+ ${BASH_SOURCE##*/}:${LINENO}: '
set -x

rg -n \
  '^\s*(requires|module|imports|syntax|rule|claim|configuration)|\[(function|total|functional|simplification|priority)' \
  /tmp/audit-work/34-unique/candidate-source/semantic.k \
  /tmp/audit-work/34-unique/candidate-source/verification.k \
  /tmp/audit-work/34-unique/candidate-source/spec.k
status=$?
set +x
printf 'EXIT_STATUS=%s\n' "$status"
exit "$status"
