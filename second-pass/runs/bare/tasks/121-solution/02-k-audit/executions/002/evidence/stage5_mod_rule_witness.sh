#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/121-solution-audit
status=0

printf '$ python3 %q %q > %q\n' \
  "$scratch/reference/py2mpy.py" \
  /audit-output/evidence/solution_mod_rule_witness.py \
  "$scratch/solution-mod-rule-witness.mpy"
python3 "$scratch/reference/py2mpy.py" \
  /audit-output/evidence/solution_mod_rule_witness.py \
  > "$scratch/solution-mod-rule-witness.mpy"
rc=$?
printf '[exit %d]\n' "$rc"
if [ "$rc" -ne 0 ]; then
  status=1
fi

printf '$ sed -n 1,100p %q\n' "$scratch/solution-mod-rule-witness.mpy"
sed -n 1,100p "$scratch/solution-mod-rule-witness.mpy"
rc=$?
printf '[exit %d]\n' "$rc"
if [ "$rc" -ne 0 ]; then
  status=1
fi

printf '$ python3 %q\n' /audit-output/evidence/mod_rule_witness.py
python3 /audit-output/evidence/mod_rule_witness.py
rc=$?
printf '[exit %d]\n' "$rc"
if [ "$rc" -ne 0 ]; then
  status=1
fi

exit "$status"
