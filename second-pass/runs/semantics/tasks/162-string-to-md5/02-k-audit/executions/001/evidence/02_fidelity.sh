#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/proof-162

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return 0
}

cd "$scratch" || exit 2

printf '$ python3 py2mpy.py solution.py > solution.generated.mpy\n'
python3 py2mpy.py solution.py > solution.generated.mpy
status=$?
printf '[exit %d]\n' "$status"

run cmp -s solution.generated.mpy solution.submitted.mpy
run sha256sum solution.generated.mpy solution.submitted.mpy
run python3 /audit-output/evidence/02_differential.py
