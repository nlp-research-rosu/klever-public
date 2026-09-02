#!/usr/bin/env bash
set -u

echo "COMMAND: python3 /reference/py2mpy.py solution.py > solution.regenerated.mpy"
python3 /reference/py2mpy.py solution.py > solution.regenerated.mpy
translator_status=$?
echo "translator_status=$translator_status"

echo "COMMAND: cmp solution.regenerated.mpy solution.mpy"
cmp solution.regenerated.mpy solution.mpy
cmp_status=$?
echo "cmp_status=$cmp_status"

echo "COMMAND: sha256sum solution.py solution.mpy solution.regenerated.mpy"
sha256sum solution.py solution.mpy solution.regenerated.mpy
hash_status=$?
echo "hash_status=$hash_status"

if (( translator_status || cmp_status || hash_status )); then
  exit 1
fi
