#!/usr/bin/env bash
set +e
scratch=/tmp/audit-work/92-any-int-audit
evidence=/audit-output/evidence

printf '$ python3 /audit-output/evidence/05_rule_assessment.py > /audit-output/evidence/05_rule_assessment.md\n'
python3 "$evidence/05_rule_assessment.py" > "$evidence/05_rule_assessment.md"
status=$?
printf 'EXIT_STATUS: %d\n' "$status"

printf '$ rg -c "^-" /audit-output/evidence/05_rule_assessment.md\n'
rg -c '^-' "$evidence/05_rule_assessment.md"
status=$?
printf 'EXIT_STATUS: %d\n' "$status"

printf '$ sha256sum /audit-output/evidence/05_rule_assessment.md\n'
sha256sum "$evidence/05_rule_assessment.md"
status=$?
printf 'EXIT_STATUS: %d\n' "$status"

printf '$ sed -n "1,55p" /audit-output/evidence/05_rule_assessment.md\n'
sed -n '1,55p' "$evidence/05_rule_assessment.md"
status=$?
printf 'EXIT_STATUS: %d\n' "$status"

printf '$ python3 /audit-output/evidence/05_complex_gap_witness.py\n'
python3 "$evidence/05_complex_gap_witness.py"
status=$?
printf 'EXIT_STATUS: %d\n' "$status"

printf '$ python3 /reference/py2mpy.py /audit-output/evidence/05_complex_gap_witness.py\n'
python3 /reference/py2mpy.py "$evidence/05_complex_gap_witness.py" > "$scratch/05_complex_gap_witness.mpy" 2> "$evidence/05_complex_gap_translator.log"
status=$?
printf 'EXIT_STATUS: %d\n' "$status"
tail -n 80 "$evidence/05_complex_gap_translator.log"
if [ "$status" -eq 0 ]; then
  printf 'REPRESENTATION_GAP_RESULT: UNEXPECTED_COMPLEX_TRANSLATION\n'
  exit 1
fi
if grep -q 'Constant complex' "$evidence/05_complex_gap_translator.log"; then
  printf 'REPRESENTATION_GAP_RESULT: CONFIRMED_COMPLEX_UNREPRESENTABLE\n'
  exit 0
fi
printf 'REPRESENTATION_GAP_RESULT: WRONG_FAILURE_MODE\n'
exit 1
