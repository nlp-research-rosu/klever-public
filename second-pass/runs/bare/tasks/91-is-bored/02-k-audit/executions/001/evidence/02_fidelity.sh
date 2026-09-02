#!/usr/bin/env bash
set -u

status=0
work=/tmp/audit-work/reconstruction

printf '%s\n' 'COMMAND: nl -ba /reference/prompt.py'
nl -ba /reference/prompt.py
code=$?
printf 'EXIT: %s\n' "$code"
(( code == 0 )) || status=1

printf '%s\n' 'COMMAND: nl -ba /reference/canonical.py'
nl -ba /reference/canonical.py
code=$?
printf 'EXIT: %s\n' "$code"
(( code == 0 )) || status=1

printf '%s\n' 'COMMAND: nl -ba /tmp/audit-work/reconstruction/solution.py'
nl -ba "$work/solution.py"
code=$?
printf 'EXIT: %s\n' "$code"
(( code == 0 )) || status=1

printf '%s\n' 'COMMAND: python3 /reference/py2mpy.py /tmp/audit-work/reconstruction/solution.py > /tmp/audit-work/reconstruction/regenerated.mpy'
python3 /reference/py2mpy.py "$work/solution.py" > "$work/regenerated.mpy"
code=$?
printf 'EXIT: %s\n' "$code"
(( code == 0 )) || status=1

printf '%s\n' 'COMMAND: cmp /tmp/audit-work/reconstruction/regenerated.mpy /tmp/audit-work/reconstruction/solution.mpy'
cmp "$work/regenerated.mpy" "$work/solution.mpy"
code=$?
printf 'EXIT: %s\n' "$code"
(( code == 0 )) || status=1

printf '%s\n' 'COMMAND: sha256sum regenerated.mpy solution.mpy'
sha256sum "$work/regenerated.mpy" "$work/solution.mpy"
code=$?
printf 'EXIT: %s\n' "$code"
(( code == 0 )) || status=1

printf '%s\n' 'COMMAND: python3 /audit-output/evidence/differential_test.py'
python3 /audit-output/evidence/differential_test.py
code=$?
printf 'EXIT: %s\n' "$code"
# A mismatch is an audit finding, so retain the test's nonzero result without
# turning this evidence driver itself into an infrastructure failure.

exit "$status"
