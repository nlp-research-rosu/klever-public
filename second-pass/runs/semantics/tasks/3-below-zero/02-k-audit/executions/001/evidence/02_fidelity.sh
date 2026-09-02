#!/usr/bin/env bash
set -u

log=/audit-output/evidence/02_fidelity.log
exec > >(tee "$log") 2>&1

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  if test "$status" -ne 0; then
    exit "$status"
  fi
}

run python3 /tmp/audit-work/rebuild/trusted/py2mpy.py \
  /tmp/audit-work/rebuild/candidate/solution.py

printf '\n$ python3 trusted/py2mpy.py candidate/solution.py > candidate/solution.regenerated.mpy\n'
python3 /tmp/audit-work/rebuild/trusted/py2mpy.py \
  /tmp/audit-work/rebuild/candidate/solution.py \
  > /tmp/audit-work/rebuild/candidate/solution.regenerated.mpy
status=$?
printf '[exit %d]\n' "$status"
if test "$status" -ne 0; then
  exit "$status"
fi

run cmp --silent \
  /tmp/audit-work/rebuild/candidate/solution.regenerated.mpy \
  /tmp/audit-work/rebuild/candidate/solution.mpy
run sha256sum \
  /tmp/audit-work/rebuild/candidate/solution.regenerated.mpy \
  /tmp/audit-work/rebuild/candidate/solution.mpy
run python3 /audit-output/evidence/differential_test.py
run wc -l /audit-output/evidence/differential-inputs.jsonl
