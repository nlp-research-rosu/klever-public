#!/usr/bin/env bash
set -uo pipefail
PS4='+ ${BASH_SOURCE##*/}:${LINENO}: '
set -x

cd /tmp/audit-work/34-unique
python3 reference/py2mpy.py body-mutation.py > body-mutation.mpy
translate_status=$?
nl -ba body-mutation.py
nl -ba body-mutation.mpy

krun body-mutation.mpy \
  --definition concrete-kompiled \
  '-cARGS=ListExpr(Int(2), Int(1), Int(2))'
krun_status=$?

kprove spec-body-sensitivity.k \
  --definition proof-kompiled \
  --spec-module SPEC-BODY-SENSITIVITY
proof_status=$?

set +x
printf 'TRANSLATE_EXIT_STATUS=%s\n' "$translate_status"
printf 'MUTATED_BODY_KRUN_EXIT_STATUS=%s\n' "$krun_status"
printf 'MUTATED_BODY_PROOF_EXIT_STATUS=%s\n' "$proof_status"
if (( translate_status || krun_status || proof_status == 0 )); then
  exit 1
fi
exit 0
