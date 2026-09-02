#!/usr/bin/env bash
set -u

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

printf '$ python3 /reference/py2mpy.py /tmp/audit-work/recon/solution.py > /tmp/audit-work/recon/solution.regenerated.mpy\n'
python3 /reference/py2mpy.py /tmp/audit-work/recon/solution.py \
  > /tmp/audit-work/recon/solution.regenerated.mpy
status=$?
printf '[exit %d]\n' "$status"

run cmp /tmp/audit-work/recon/solution.regenerated.mpy /candidate/solution.mpy
run sha256sum /tmp/audit-work/recon/solution.regenerated.mpy /candidate/solution.mpy
run python3 /audit-output/evidence/differential_test.py
