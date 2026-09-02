#!/usr/bin/env bash
set -u
overall=0

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  local status=0
  "$@" || status=$?
  printf '[exit %d]\n' "$status"
  if (( status != 0 )); then
    overall=1
  fi
}

cd /tmp/audit-work/85-add || exit 1

printf '$ python3 py2mpy.py solution.py > regenerated-solution.mpy\n'
translation_status=0
python3 py2mpy.py solution.py > regenerated-solution.mpy || translation_status=$?
printf '[exit %d]\n' "$translation_status"
if (( translation_status != 0 )); then
  overall=1
fi

run cmp solution.mpy regenerated-solution.mpy
run sha256sum solution.py solution.mpy regenerated-solution.mpy
run python3 /audit-output/evidence/differential_test.py

printf 'stage2_fidelity_status=%d\n' "$overall"
exit "$overall"
