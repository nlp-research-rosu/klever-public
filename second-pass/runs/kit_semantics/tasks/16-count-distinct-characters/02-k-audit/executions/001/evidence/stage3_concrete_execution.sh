#!/usr/bin/env bash
set -u
set -o pipefail

exec > >(tee /audit-output/evidence/stage3-concrete-execution.log) 2>&1
set -x

cd /tmp/audit-work/reconstruction || exit 90

krun audit_concrete.mpy --definition runtime-audit-kompiled \
  > /audit-output/evidence/stage3-concrete-final-config.txt
krun_status=$?
printf 'fresh_concrete_krun_exit=%d\n' "$krun_status"

grep -F '"result_empty" |-> 0' \
  /audit-output/evidence/stage3-concrete-final-config.txt
empty_status=$?
printf 'empty_result_check_exit=%d\n' "$empty_status"

grep -F '"result_xyz" |-> 3' \
  /audit-output/evidence/stage3-concrete-final-config.txt
xyz_status=$?
printf 'xyz_result_check_exit=%d\n' "$xyz_status"

grep -F '"result_jerry" |-> 4' \
  /audit-output/evidence/stage3-concrete-final-config.txt
jerry_status=$?
printf 'jerry_result_check_exit=%d\n' "$jerry_status"

grep -F '"result_case_pair" |-> 1' \
  /audit-output/evidence/stage3-concrete-final-config.txt
case_pair_status=$?
printf 'case_pair_result_check_exit=%d\n' "$case_pair_status"

grep -F '"result_punctuation" |-> 5' \
  /audit-output/evidence/stage3-concrete-final-config.txt
punctuation_status=$?
printf 'punctuation_result_check_exit=%d\n' "$punctuation_status"

if [[ "$krun_status" -ne 0 ]] ||
   [[ "$empty_status" -ne 0 ]] ||
   [[ "$xyz_status" -ne 0 ]] ||
   [[ "$jerry_status" -ne 0 ]] ||
   [[ "$case_pair_status" -ne 0 ]] ||
   [[ "$punctuation_status" -ne 0 ]]; then
  exit 1
fi
