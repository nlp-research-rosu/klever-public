#!/usr/bin/env bash
set -u

translation_tmp=$(mktemp /tmp/audit-work/translated.XXXXXX.mpy)
trap 'rm -f "$translation_tmp"' EXIT

python3 /reference/py2mpy.py /tmp/audit-work/source/solution.py >"$translation_tmp"
translator_status=$?
printf 'translator_exit=%d\n' "$translator_status"
sha256sum "$translation_tmp" /tmp/audit-work/source/solution.mpy
if cmp -s "$translation_tmp" /tmp/audit-work/source/solution.mpy; then
  printf '%s\n' 'BYTE_IDENTITY=YES'
  exit "$translator_status"
fi
printf '%s\n' 'BYTE_IDENTITY=NO'
cmp -l "$translation_tmp" /tmp/audit-work/source/solution.mpy | head -n 20
exit 1
