#!/usr/bin/env bash
set -o pipefail

cd /tmp/audit-work/122-add-elements || exit 70

printf '%s\n' \
  'COMMAND: python3 /reference/py2mpy.py audit_boundary.py > audit_boundary.mpy'
python3 /reference/py2mpy.py audit_boundary.py > audit_boundary.mpy
translate_status=$?
printf 'TRANSLATE_EXIT_STATUS: %d\n' "$translate_status"
if [[ "$translate_status" -ne 0 ]]; then
  exit "$translate_status"
fi

printf '%s\n' \
  'COMMAND: kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition runtime-audit-kompiled'
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-audit-kompiled
kompile_status=$?
printf 'KOMPILE_EXIT_STATUS: %d\n' "$kompile_status"
if [[ "$kompile_status" -ne 0 ]]; then
  exit "$kompile_status"
fi

printf '%s\n' \
  'COMMAND: krun audit_boundary.mpy --definition runtime-audit-kompiled'
krun audit_boundary.mpy --definition runtime-audit-kompiled
krun_status=$?
printf 'KRUN_EXIT_STATUS: %d\n' "$krun_status"
exit "$krun_status"
