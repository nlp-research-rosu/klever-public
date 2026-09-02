#!/usr/bin/env bash
set -uo pipefail

SCRATCH=/tmp/audit-work/59-lpf
EVIDENCE=/audit-output/evidence
cd "$SCRATCH" || exit 1

echo "$ python3 /reference/py2mpy.py operational-context.py > operational-context.mpy"
python3 /reference/py2mpy.py operational-context.py > operational-context.mpy
translate_status=$?
echo "translator_exit=$translate_status"
if [ "$translate_status" -ne 0 ]; then
  exit "$translate_status"
fi

echo "$ krun operational-context.mpy --definition audit-runtime-kompiled"
krun operational-context.mpy \
  --definition audit-runtime-kompiled \
  > "$EVIDENCE/07_fixed_semantics_krun.log" 2>&1
fixed_status=$?
echo "fixed_krun_exit=$fixed_status"

echo "$ krun operational-context.mpy --definition audit-verification-kompiled"
krun operational-context.mpy \
  --definition audit-verification-kompiled \
  > "$EVIDENCE/07_extended_semantics_krun.log" 2>&1
extended_status=$?
echo "extended_krun_exit=$extended_status"

echo "$ diff -u 07_fixed_semantics_krun.log 07_extended_semantics_krun.log"
diff -u \
  "$EVIDENCE/07_fixed_semantics_krun.log" \
  "$EVIDENCE/07_extended_semantics_krun.log" \
  > "$EVIDENCE/07_fixed_vs_extended.diff"
diff_status=$?
echo "diff_exit=$diff_status"

echo "fixed_output_tail:"
tail -80 "$EVIDENCE/07_fixed_semantics_krun.log"
echo "extended_output_tail:"
tail -80 "$EVIDENCE/07_extended_semantics_krun.log"

if [ "$fixed_status" -ne 0 ] || [ "$extended_status" -ne 0 ]; then
  echo "ERROR: one operational run failed"
  exit 1
fi
if [ "$diff_status" -ne 0 ]; then
  echo "ERROR: fixed and extended final configurations differ"
  tail -160 "$EVIDENCE/07_fixed_vs_extended.diff"
  exit 1
fi
echo "fixed_and_extended_outputs_identical=true"
