#!/usr/bin/env bash
set -uo pipefail

status=0
run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  rc=$?
  printf '[exit %d]\n' "$rc"
  if (( rc != 0 )); then status=1; fi
}

printf 'Trusted and candidate source hashes:\n'
run sha256sum \
  /reference/prompt.py /reference/canonical.py /reference/py2mpy.py \
  /candidate/solution.py /candidate/solution.mpy

printf '\nRegenerate using the trusted translator in isolated scratch:\n'
printf '\n$ python3 py2mpy.py solution.py > regenerated-solution.mpy\n'
(cd /tmp/audit-work/maximum-120-audit &&
  python3 py2mpy.py solution.py > regenerated-solution.mpy)
rc=$?
printf '[exit %d]\n' "$rc"
if (( rc != 0 )); then status=1; fi
run cmp /candidate/solution.mpy /tmp/audit-work/maximum-120-audit/regenerated-solution.mpy
run sha256sum /candidate/solution.mpy /tmp/audit-work/maximum-120-audit/regenerated-solution.mpy

printf '\nIndependent Python differential:\n'
run python3 /audit-output/evidence/differential_test.py
run sha256sum /audit-output/evidence/differential-inputs.jsonl
run wc -l -c /audit-output/evidence/differential-inputs.jsonl

exit "$status"
