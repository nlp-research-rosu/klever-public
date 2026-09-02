#!/usr/bin/env bash
set -u

cd /tmp/audit-work/147-get-max-triples-clean || exit 1
status=0

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  rc=$?
  printf '[exit %d]\n' "$rc"
  if (( rc != 0 )); then
    status=1
  fi
}

printf '$ python3 py2mpy.py solution.py > regenerated-solution.mpy\n'
python3 py2mpy.py solution.py > regenerated-solution.mpy
rc=$?
printf '[exit %d]\n' "$rc"
if (( rc != 0 )); then
  status=1
fi

run cmp -s regenerated-solution.mpy solution.mpy
run sha256sum regenerated-solution.mpy solution.mpy
run python3 differential_test.py
run python3 compare_program_term.py

printf 'FINAL_STATUS=%d\n' "$status"
exit "$status"
