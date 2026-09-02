#!/usr/bin/env bash
set -u

trusted=/tmp/audit-work/159-eat/trusted/py2mpy.py
source_file=/tmp/audit-work/159-eat/candidate-src/solution.py
submitted=/tmp/audit-work/159-eat/candidate-src/solution.mpy

if cmp -s <(python3 "$trusted" "$source_file") "$submitted"; then
  printf 'BYTE_IDENTITY=YES\n'
  status=0
else
  printf 'BYTE_IDENTITY=NO\n'
  status=1
fi

printf 'TRUSTED_TRANSLATOR_OUTPUT_SHA256='
python3 "$trusted" "$source_file" | sha256sum
printf 'SUBMITTED_MPY_SHA256='
sha256sum "$submitted"
exit "$status"
