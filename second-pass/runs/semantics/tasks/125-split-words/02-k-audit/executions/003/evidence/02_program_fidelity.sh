#!/usr/bin/env bash
set -u
set -o pipefail

cd /tmp/audit-work/125-split-words

echo '$ python3 py2mpy.py solution.py > regenerated-solution.mpy'
python3 py2mpy.py solution.py > regenerated-solution.mpy
echo "translator_exit=$?"

echo '$ cmp regenerated-solution.mpy solution.mpy'
cmp regenerated-solution.mpy solution.mpy
echo "translation_cmp_exit=$?"

echo '$ sha256sum solution.mpy regenerated-solution.mpy'
sha256sum solution.mpy regenerated-solution.mpy
echo "translation_hash_exit=$?"

echo '$ python3 /audit-output/evidence/02_differential.py'
python3 /audit-output/evidence/02_differential.py
echo "differential_exit=$?"
