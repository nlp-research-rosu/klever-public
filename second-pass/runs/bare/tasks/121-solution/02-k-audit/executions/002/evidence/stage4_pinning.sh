#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/121-solution-audit
status=0

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  rc=$?
  printf '[exit %d]\n' "$rc"
  if [ "$rc" -ne 0 ]; then
    status=1
  fi
}

run python3 /audit-output/evidence/program_pinning.py

printf '$ python3 %q %q > %q\n' \
  "$scratch/reference/py2mpy.py" \
  /audit-output/evidence/solution_body_mutation.py \
  "$scratch/solution-body-mutation.mpy"
python3 "$scratch/reference/py2mpy.py" \
  /audit-output/evidence/solution_body_mutation.py \
  > "$scratch/solution-body-mutation.mpy"
rc=$?
printf '[exit %d]\n' "$rc"
if [ "$rc" -ne 0 ]; then
  status=1
fi

printf '$ cmp -- %q %q\n' \
  "$scratch/candidate/solution.mpy" "$scratch/solution-body-mutation.mpy"
cmp -- "$scratch/candidate/solution.mpy" "$scratch/solution-body-mutation.mpy"
rc=$?
printf '[exit %d; expected nonzero because the translated body changed]\n' "$rc"
if [ "$rc" -eq 0 ]; then
  status=1
fi
run sed -n 1,80p "$scratch/solution-body-mutation.mpy"

exit "$status"
