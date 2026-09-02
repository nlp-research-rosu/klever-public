#!/usr/bin/env bash
set -u

run() {
  echo "\$ $*"
  "$@"
  status=$?
  echo "[exit $status]"
  return "$status"
}

run nl -ba /reference/prompt.py
run nl -ba /reference/canonical.py
run nl -ba /tmp/audit-work/candidate/solution.py
run nl -ba /tmp/audit-work/candidate/solution.mpy

echo '$ cd /tmp/audit-work/candidate && python3 /tmp/audit-work/trusted/py2mpy.py solution.py > /tmp/audit-work/regenerated-solution.mpy'
(
  cd /tmp/audit-work/candidate || exit 1
  python3 /tmp/audit-work/trusted/py2mpy.py solution.py \
    > /tmp/audit-work/regenerated-solution.mpy
)
status=$?
echo "[exit $status]"

run cmp \
  /tmp/audit-work/candidate/solution.mpy \
  /tmp/audit-work/regenerated-solution.mpy
run sha256sum \
  /tmp/audit-work/candidate/solution.mpy \
  /tmp/audit-work/regenerated-solution.mpy
run python3 /audit-output/evidence/differential_test.py
