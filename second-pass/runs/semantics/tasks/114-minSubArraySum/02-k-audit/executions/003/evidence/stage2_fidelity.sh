#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/114-minSubArraySum

printf '$ python3 py2mpy.py solution.py > regenerated.mpy\n'
(
  cd "$scratch" || exit 1
  python3 py2mpy.py solution.py > regenerated.mpy
)
status=$?
printf '[exit %d]\n' "$status"

printf '$ cmp -s regenerated.mpy solution.mpy\n'
(
  cd "$scratch" || exit 1
  cmp -s regenerated.mpy solution.mpy
)
status=$?
printf '[exit %d]\n' "$status"

printf '$ sha256sum solution.py solution.mpy regenerated.mpy py2mpy.py canonical.py prompt.py\n'
(
  cd "$scratch" || exit 1
  sha256sum solution.py solution.mpy regenerated.mpy py2mpy.py canonical.py prompt.py
)
status=$?
printf '[exit %d]\n' "$status"

printf '$ python3 /audit-output/evidence/differential_test.py\n'
python3 /audit-output/evidence/differential_test.py
status=$?
printf '[exit %d]\n' "$status"
