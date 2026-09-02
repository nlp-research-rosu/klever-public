#!/usr/bin/env bash
set -u
cd /tmp/audit-work/reconstruction

printf '$ python3 /reference/py2mpy.py solution.py > solution.regenerated.mpy\n'
python3 /reference/py2mpy.py solution.py > solution.regenerated.mpy
status=$?
printf '[exit %d]\n' "$status"

printf '\n$ cmp -s solution.regenerated.mpy solution.mpy\n'
cmp -s solution.regenerated.mpy solution.mpy
status=$?
printf '[exit %d]\n' "$status"

printf '\n$ sha256sum solution.py solution.mpy solution.regenerated.mpy\n'
sha256sum solution.py solution.mpy solution.regenerated.mpy
status=$?
printf '[exit %d]\n' "$status"

printf '\n$ python3 /audit-output/evidence/02_differential.py\n'
python3 /audit-output/evidence/02_differential.py
status=$?
printf '[exit %d]\n' "$status"
exit "$status"
