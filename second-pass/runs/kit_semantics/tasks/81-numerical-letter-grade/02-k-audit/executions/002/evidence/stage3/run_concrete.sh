#!/usr/bin/env bash
set -u

cd /tmp/audit-work/candidate-src || exit 90

printf '$ python3 /audit-output/evidence/stage3/check_concrete_function.py\n'
python3 /audit-output/evidence/stage3/check_concrete_function.py
ast_rc=$?
printf 'EXIT ast_identity=%s\n' "$ast_rc"

printf '$ python3 /reference/py2mpy.py /audit-output/evidence/stage3/concrete_audit.py > concrete_audit.mpy\n'
python3 /reference/py2mpy.py /audit-output/evidence/stage3/concrete_audit.py > concrete_audit.mpy
translate_rc=$?
printf 'EXIT translate=%s\n' "$translate_rc"

printf '$ krun concrete_audit.mpy --definition audit-runtime-kompiled\n'
krun concrete_audit.mpy --definition audit-runtime-kompiled
krun_rc=$?
printf 'EXIT krun=%s\n' "$krun_rc"

if (( ast_rc != 0 || translate_rc != 0 || krun_rc != 0 )); then
  exit 1
fi
exit 0
