#!/usr/bin/env bash
set -u

cd /tmp/audit-work/run-118 || exit 70
overall=0

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  rc=$?
  printf '[exit %d]\n' "$rc"
  if (( rc != 0 )); then
    overall=1
  fi
}

echo '== Regenerate the submitted MPY with the trusted translator =='
printf '\n$ python3 trusted-py2mpy.py solution.py > regenerated-solution.mpy\n'
python3 trusted-py2mpy.py solution.py > regenerated-solution.mpy
rc=$?
printf '[exit %d]\n' "$rc"
(( rc == 0 )) || overall=1
run cmp -s regenerated-solution.mpy solution.mpy
run sha256sum regenerated-solution.mpy solution.mpy
run diff -u solution.mpy regenerated-solution.mpy

echo '== Independent canonical-versus-candidate differential =='
run python3 /audit-output/evidence/differential_test.py

exit "$overall"
