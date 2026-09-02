#!/usr/bin/env bash
set -u

work=/tmp/audit-work/92-any-int
log=/audit-output/evidence/05_program_sensitivity.log
exec > >(tee "$log") 2>&1

printf 'AUDIT_STAGE: 5 body-sensitivity check for the program-pinning macro\n'

printf '\nCOMMAND: python3 %q %q > %q\n' \
  "$work/trusted/py2mpy.py" \
  "$work/generated/solution-body-mutation.py" \
  "$work/generated/solution-body-mutation.mpy"
python3 "$work/trusted/py2mpy.py" \
  "$work/generated/solution-body-mutation.py" \
  > "$work/generated/solution-body-mutation.mpy"
translate_status=$?
printf 'EXIT_STATUS: %d\n' "$translate_status"

printf '\nCOMMAND: kast -d %q -m ANY-INT-VERIFICATION -s Program --expand-macros -o kore %q > %q\n' \
  "$work/proof-kompiled" \
  "$work/generated/solution-body-mutation.mpy" \
  "$work/generated/solution-body-mutation.kore"
kast -d "$work/proof-kompiled" \
  -m ANY-INT-VERIFICATION -s Program \
  --expand-macros -o kore \
  "$work/generated/solution-body-mutation.mpy" \
  > "$work/generated/solution-body-mutation.kore"
kast_status=$?
printf 'EXIT_STATUS: %d\n' "$kast_status"

printf '\nCOMMAND: cmp -s %q %q\n' \
  "$work/generated/solution-body-mutation.kore" \
  "$work/generated/wrapper-program.kore"
cmp -s \
  "$work/generated/solution-body-mutation.kore" \
  "$work/generated/wrapper-program.kore"
compare_status=$?
printf 'EXIT_STATUS: %d\n' "$compare_status"
if [ "$compare_status" -ne 0 ]; then
  printf 'EXPECTED_PROGRAM_IDENTITY_REJECTION: present\n'
else
  printf 'EXPECTED_PROGRAM_IDENTITY_REJECTION: missing\n'
fi

sha256sum \
  "$work/generated/solution-body-mutation.kore" \
  "$work/generated/wrapper-program.kore"

printf '\nCOMMAND: python3 -c <execute original and body mutation at (1,2,3)>\n'
python3 -c 'import runpy; o=runpy.run_path("/tmp/audit-work/92-any-int/src/solution.py")["any_int"](1,2,3); m=runpy.run_path("/tmp/audit-work/92-any-int/generated/solution-body-mutation.py")["any_int"](1,2,3); print("original=",o,"mutated=",m); raise SystemExit(0 if o is True and m is False else 1)'
python_status=$?
printf 'EXIT_STATUS: %d\n' "$python_status"

if [ "$translate_status" -eq 0 ] \
   && [ "$kast_status" -eq 0 ] \
   && [ "$compare_status" -ne 0 ] \
   && [ "$python_status" -eq 0 ]; then
  printf 'BODY_SENSITIVITY_RESULT: PASS\n'
  exit 0
fi

printf 'BODY_SENSITIVITY_RESULT: FAIL\n'
exit 1
