#!/usr/bin/env bash
set +e
scratch=/tmp/audit-work/92-any-int-audit

printf '$ python3 /reference/py2mpy.py /tmp/audit-work/92-any-int-audit/solution.py > /tmp/audit-work/92-any-int-audit/regenerated-solution.mpy\n'
python3 /reference/py2mpy.py "$scratch/solution.py" > "$scratch/regenerated-solution.mpy"
status=$?
printf 'EXIT_STATUS: %d\n' "$status"

printf '$ cmp -s /tmp/audit-work/92-any-int-audit/regenerated-solution.mpy /candidate/solution.mpy\n'
cmp -s "$scratch/regenerated-solution.mpy" /candidate/solution.mpy
status=$?
printf 'EXIT_STATUS: %d\n' "$status"

printf '$ sha256sum /tmp/audit-work/92-any-int-audit/regenerated-solution.mpy /candidate/solution.mpy\n'
sha256sum "$scratch/regenerated-solution.mpy" /candidate/solution.mpy
status=$?
printf 'EXIT_STATUS: %d\n' "$status"

printf '$ python3 /audit-output/evidence/02_differential.py\n'
python3 /audit-output/evidence/02_differential.py
status=$?
printf 'EXIT_STATUS: %d\n' "$status"

exit 0
