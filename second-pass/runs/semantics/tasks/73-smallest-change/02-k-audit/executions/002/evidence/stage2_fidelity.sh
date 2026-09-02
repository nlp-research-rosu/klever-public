#!/usr/bin/env bash
set -euo pipefail

scratch=/tmp/audit-work/73-smallest-change

echo 'TRANSLATE_COMMAND: python3 trusted-py2mpy.py solution.py > solution.regenerated.mpy'
(
  cd "$scratch"
  python3 trusted-py2mpy.py solution.py > solution.regenerated.mpy
)

echo 'COMPARE_COMMAND: cmp --silent solution.regenerated.mpy solution.mpy'
(
  cd "$scratch"
  cmp --silent solution.regenerated.mpy solution.mpy
)

sha256sum "$scratch/solution.py" \
  "$scratch/solution.mpy" \
  "$scratch/solution.regenerated.mpy"
echo 'BYTE_IDENTITY: true'
