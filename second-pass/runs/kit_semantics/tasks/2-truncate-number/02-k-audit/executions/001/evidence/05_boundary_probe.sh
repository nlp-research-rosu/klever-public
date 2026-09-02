#!/usr/bin/env bash
set -u

work=/tmp/audit-work/candidate
translator=/tmp/audit-work/py2mpy.py

for stem in auditor-boundary-subnormal auditor-boundary-below-one auditor-boundary-above-one; do
  python3 "$translator" "$work/$stem.py" > "$work/$stem.mpy"
  translate_status=$?
  echo "TRANSLATE $stem exit=$translate_status"
  krun "$work/$stem.mpy" --definition "$work/fresh-runtime-kompiled"
  krun_status=$?
  echo "KRUN $stem exit=$krun_status"
done

exit 0
