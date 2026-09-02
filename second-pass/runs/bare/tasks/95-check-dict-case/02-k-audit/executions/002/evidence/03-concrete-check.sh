#!/usr/bin/env bash
set -u

printf '%s\n' \
  'COMMAND: python3 k_concrete_differential.py /tmp/audit-work/95-check-dict-case-audit'
PYTHONDONTWRITEBYTECODE=1 python3 \
  /audit-output/evidence/k_concrete_differential.py \
  /tmp/audit-work/95-check-dict-case-audit
command_status=$?
printf 'CONCRETE_DIFFERENTIAL_EXIT=%s\n' "$command_status"
exit "$command_status"
