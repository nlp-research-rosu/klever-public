#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/160-do-algebra
output=/audit-output/evidence/05_eval_bridge_krun.out

echo "COMMAND: python3 /audit-output/evidence/05_make_eval_cases.py"
python3 /audit-output/evidence/05_make_eval_cases.py || exit $?

echo "COMMAND: python3 py2mpy.py 05_eval_cases.py > 05_eval_cases.mpy"
(
  cd "$scratch" || exit 90
  python3 py2mpy.py 05_eval_cases.py > 05_eval_cases.mpy
)
translate_status=$?
echo "TRANSLATOR_EXIT_STATUS=$translate_status"
if (( translate_status != 0 )); then
  exit "$translate_status"
fi

echo "COMMAND: krun 05_eval_cases.mpy --definition audit-runtime-kompiled > $output"
(
  cd "$scratch" || exit 91
  krun 05_eval_cases.mpy --definition audit-runtime-kompiled > "$output"
)
krun_status=$?
echo "KRUN_EXIT_STATUS=$krun_status"
if (( krun_status != 0 )); then
  exit "$krun_status"
fi

echo "COMMAND: python3 /audit-output/evidence/05_check_eval_output.py"
python3 /audit-output/evidence/05_check_eval_output.py
check_status=$?
echo "CHECK_EXIT_STATUS=$check_status"
exit "$check_status"
