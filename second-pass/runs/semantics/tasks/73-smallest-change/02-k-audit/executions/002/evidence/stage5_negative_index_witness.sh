#!/usr/bin/env bash
set -euo pipefail

scratch=/tmp/audit-work/73-smallest-change
cd "$scratch"

echo 'TRANSLATE_COMMAND: python3 trusted-py2mpy.py negative-index-witness.py > negative-index-witness.mpy'
python3 trusted-py2mpy.py negative-index-witness.py > negative-index-witness.mpy

echo 'PYTHON_COMMAND: python3 negative-index-witness.py'
python3 negative-index-witness.py
echo 'PYTHON_FIXED_RESULT: helper([5], -1, 0) == 0'

echo 'KRUN_COMMAND: krun negative-index-witness.mpy --definition audit-runtime-kompiled'
krun negative-index-witness.mpy --definition audit-runtime-kompiled
echo 'KRUN_FIXED_ASSERTION: passed'
