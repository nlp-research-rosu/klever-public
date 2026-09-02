#!/usr/bin/env bash
set -euo pipefail

printf '%s\n' 'COMMAND: nl -ba candidate K sources'
nl -ba /candidate/semantic.k
nl -ba /candidate/verification.k
nl -ba /candidate/spec.k

printf '%s\n' 'COMMAND: rg declarations and rules'
rg -n '^[[:space:]]*(configuration|syntax|rule|claim|requires|imports)' \
  /candidate/semantic.k \
  /candidate/verification.k \
  /candidate/spec.k

printf '%s\n' 'COMMAND: scan trust-sensitive attributes and markers'
set +e
rg -n '\[(total|functional|simplification|concrete|trusted|priority|owise)|opaque|--trusted' \
  /candidate/semantic.k \
  /candidate/verification.k \
  /candidate/spec.k \
  /candidate/prove.sh
scan_status=$?
set -e
printf 'ATTRIBUTE_SCAN_EXIT_STATUS=%s EXPECTED_1_FOR_NO_MATCH=true\n' "$scan_status"
test "$scan_status" -eq 1

printf 'EXIT_STATUS=0\n'
