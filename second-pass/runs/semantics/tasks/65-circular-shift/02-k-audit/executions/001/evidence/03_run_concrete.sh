#!/usr/bin/env bash
set -u
cd /tmp/audit-work/case || exit 125

printf '$ python3 /tmp/audit-work/trusted/py2mpy.py /audit-output/evidence/03_reviewer_concrete.py > reviewer-concrete.mpy\n'
python3 /tmp/audit-work/trusted/py2mpy.py \
  /audit-output/evidence/03_reviewer_concrete.py > reviewer-concrete.mpy
translate_rc=$?
printf '[exit %d]\n' "$translate_rc"
if test "$translate_rc" -ne 0; then
  exit "$translate_rc"
fi

printf '$ krun reviewer-concrete.mpy --definition runtime-kompiled --output pretty\n'
krun reviewer-concrete.mpy \
  --definition runtime-kompiled \
  --output pretty
run_rc=$?
printf '[exit %d]\n' "$run_rc"
exit "$run_rc"
