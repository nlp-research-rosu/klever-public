#!/usr/bin/env bash
set -uo pipefail

audit_generated=/tmp/audit-work/palindrome-audit/regenerated-solution.mpy

printf 'COMMAND: python3 %q %q > %q\n' \
  /reference/py2mpy.py \
  /tmp/audit-work/palindrome-audit/candidate/solution.py \
  "$audit_generated"
python3 /reference/py2mpy.py \
  /tmp/audit-work/palindrome-audit/candidate/solution.py \
  > "$audit_generated"
audit_translate_status=$?
printf 'TRANSLATOR_EXIT_STATUS: %d\n' "$audit_translate_status"

printf 'COMMAND: cmp %q %q\n' \
  "$audit_generated" \
  /tmp/audit-work/palindrome-audit/candidate/solution.mpy
cmp "$audit_generated" /tmp/audit-work/palindrome-audit/candidate/solution.mpy
audit_cmp_status=$?
printf 'CMP_EXIT_STATUS: %d\n' "$audit_cmp_status"

sha256sum \
  "$audit_generated" \
  /tmp/audit-work/palindrome-audit/candidate/solution.mpy

if (( audit_translate_status != 0 )); then
  exit "$audit_translate_status"
fi
exit "$audit_cmp_status"
