#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/52-below-threshold
echo 'COMMAND: python3 py2mpy.py k-concrete-audit.py > k-concrete-audit.mpy'
(
  cd "$scratch" || exit 72
  python3 py2mpy.py k-concrete-audit.py > k-concrete-audit.mpy
)
status=$?
echo "TRANSLATE_EXIT=$status"
sha256sum "$scratch/k-concrete-audit.py" "$scratch/k-concrete-audit.mpy"
echo "EXIT_STATUS=$status"
exit "$status"
