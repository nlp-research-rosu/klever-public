#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/145-order-by-points-002
evidence=/audit-output/evidence
overall=0

echo "$ python3 $evidence/reverse_stability_probe.py"
python3 "$evidence/reverse_stability_probe.py"
python_status=$?
echo "EXIT (CPython expected success): $python_status"
if [ "$python_status" -ne 0 ]; then overall=1; fi

echo "$ cd $scratch"
cd "$scratch" || exit 1
echo "EXIT: 0"

echo "$ python3 /reference/py2mpy.py $evidence/reverse_stability_probe.py > reverse_stability_probe.mpy"
python3 /reference/py2mpy.py \
  "$evidence/reverse_stability_probe.py" \
  > reverse_stability_probe.mpy
translation_status=$?
echo "EXIT (translation): $translation_status"
if [ "$translation_status" -ne 0 ]; then overall=1; fi

echo "$ krun reverse_stability_probe.mpy --definition audit-runtime-kompiled"
krun reverse_stability_probe.mpy \
  --definition audit-runtime-kompiled \
  2>&1 | tee "$evidence/stage5_reverse_stability_krun.log"
krun_status=${PIPESTATUS[0]}
echo "EXIT (krun process, expected nonzero): $krun_status"
if [ "$krun_status" -eq 0 ] || [ "$krun_status" -eq 124 ]; then
  echo "UNEXPECTED concrete-semantics reverse probe status"
  overall=1
fi
if ! rg -U -q '<exc>[[:space:]]+AssertionError[[:space:]]+</exc>' \
    "$evidence/stage5_reverse_stability_krun.log"; then
  echo "MISSING expected concrete-semantics reverse-stability discrepancy"
  overall=1
fi
if ! rg -U -q '<exit-code>[[:space:]]+1[[:space:]]+</exit-code>' \
    "$evidence/stage5_reverse_stability_krun.log"; then
  echo "MISSING expected modeled exit-code 1"
  overall=1
fi

echo "STAGE5 REVERSE PROBE EXIT: $overall"
exit "$overall"
