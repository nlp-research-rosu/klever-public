#!/usr/bin/env bash
set -u

task_dir=/tmp/audit-work/139-special-factorial

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  rc=$?
  printf '[exit %d]\n' "$rc"
  return 0
}

printf 'STAGE 4 REAL-PROGRAM PINNING AND GROUND WITNESSES\n'
run python3 /audit-output/evidence/pinning_check.py
run python3 /audit-output/evidence/stage4_witness.py

printf '$ python3 /reference/py2mpy.py /audit-output/evidence/ground_driver.py > %q\n' \
  "$task_dir/ground_driver.mpy"
python3 /reference/py2mpy.py /audit-output/evidence/ground_driver.py \
  > "$task_dir/ground_driver.mpy"
rc=$?
printf '[exit %d]\n' "$rc"

run krun "$task_dir/ground_driver.mpy" \
  --definition "$task_dir/runtime-kompiled" \
  --output pretty
