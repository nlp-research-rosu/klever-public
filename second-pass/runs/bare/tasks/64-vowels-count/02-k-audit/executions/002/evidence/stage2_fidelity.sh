#!/usr/bin/env bash
set -euo pipefail
set -x

cd /tmp/audit-work/64-vowels-count
python3 trusted-py2mpy.py solution.py > regenerated.solution.mpy
cmp -s regenerated.solution.mpy solution.mpy
printf 'translator_byte_identity=true\n'
sha256sum solution.py solution.mpy regenerated.solution.mpy \
  trusted-canonical.py trusted-prompt.py trusted-py2mpy.py
python3 /audit-output/evidence/differential_test.py

