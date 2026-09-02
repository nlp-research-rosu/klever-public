#!/usr/bin/env bash
set -euo pipefail

scratch=/tmp/audit-work/73-smallest-change
cd "$scratch"

echo 'TRANSLATE_COMMAND: python3 trusted-py2mpy.py nested-list-witness.py > nested-list-witness.mpy'
python3 trusted-py2mpy.py nested-list-witness.py > nested-list-witness.mpy

echo 'PYTHON_COMMAND: python3 nested-list-witness.py'
python3 nested-list-witness.py
echo 'PYTHON_FIXED_RESULT: smallest_change([[5], [5]]) == 0'

echo 'KRUN_COMMAND: krun nested-list-witness.mpy --definition audit-runtime-kompiled'
krun nested-list-witness.mpy --definition audit-runtime-kompiled
echo 'KRUN_FIXED_ASSERTION: passed'
