#!/usr/bin/env bash
set -uo pipefail
PS4='+ ${BASH_SOURCE##*/}:${LINENO}: '
set -x

cmp -s /candidate/prompt.py /reference/prompt.py
prompt_status=$?
cmp -s /candidate/py2mpy.py /reference/py2mpy.py
translator_status=$?
python3 /tmp/audit-work/34-unique/reference/py2mpy.py \
  /tmp/audit-work/34-unique/candidate-source/solution.py \
  > /tmp/audit-work/34-unique/regenerated-solution.mpy
translate_status=$?
cmp -s /tmp/audit-work/34-unique/regenerated-solution.mpy \
  /tmp/audit-work/34-unique/candidate-source/solution.mpy
mpy_status=$?
sha256sum \
  /candidate/prompt.py /reference/prompt.py \
  /candidate/py2mpy.py /reference/py2mpy.py \
  /tmp/audit-work/34-unique/candidate-source/solution.py \
  /tmp/audit-work/34-unique/candidate-source/solution.mpy \
  /tmp/audit-work/34-unique/regenerated-solution.mpy
hash_status=$?
set +x
printf 'PROMPT_CMP_STATUS=%s\n' "$prompt_status"
printf 'TRANSLATOR_CMP_STATUS=%s\n' "$translator_status"
printf 'TRANSLATE_STATUS=%s\n' "$translate_status"
printf 'MPY_CMP_STATUS=%s\n' "$mpy_status"
printf 'HASH_STATUS=%s\n' "$hash_status"

if (( prompt_status || translator_status || translate_status || mpy_status || hash_status )); then
  exit 1
fi
exit 0
