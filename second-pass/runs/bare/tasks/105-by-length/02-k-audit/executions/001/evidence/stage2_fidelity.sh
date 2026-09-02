#!/usr/bin/env bash
set +e
set -x

cd /tmp/audit-work/source || exit 90

python3 /reference/py2mpy.py solution.py > /tmp/audit-work/runs/regenerated-solution.mpy
translator_exit=$?
printf 'trusted translator exit: %s\n' "$translator_exit"
cmp /tmp/audit-work/runs/regenerated-solution.mpy solution.mpy
identity_exit=$?
printf 'regenerated-vs-submitted byte comparison exit: %s\n' "$identity_exit"
sha256sum /tmp/audit-work/runs/regenerated-solution.mpy solution.mpy

python3 /audit-output/evidence/differential_test.py
differential_exit=$?
printf 'differential test exit: %s\n' "$differential_exit"
wc -lc /audit-output/evidence/differential_inputs.jsonl
sha256sum /audit-output/evidence/differential_inputs.jsonl

if [ "$translator_exit" -ne 0 ] || [ "$identity_exit" -ne 0 ] || [ "$differential_exit" -ne 0 ]; then
  exit 1
fi
exit 0
