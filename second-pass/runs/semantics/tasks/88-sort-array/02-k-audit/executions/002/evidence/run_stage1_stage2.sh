#!/usr/bin/env bash
set -uo pipefail

evidence_dir=/audit-output/evidence
scratch_dir=/tmp/audit-work/88-sort-array
log_file="$evidence_dir/stage1_stage2.log"

run() {
  local command_text=$1
  printf '\n$ %s\n' "$command_text"
  bash -o pipefail -c "$command_text"
  local status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

{
  run "python3 $evidence_dir/integrity_check.py" || exit $?
  run "python3 $scratch_dir/py2mpy.py $scratch_dir/solution.py > $scratch_dir/regenerated-solution.mpy" || exit $?
  run "cmp -s $scratch_dir/regenerated-solution.mpy $scratch_dir/solution.mpy" || exit $?
  run "sha256sum $scratch_dir/regenerated-solution.mpy $scratch_dir/solution.mpy" || exit $?
  run "python3 $evidence_dir/differential_test.py" || exit $?
} 2>&1 | tee "$log_file"
status=${PIPESTATUS[0]}
printf 'SCRIPT_EXIT=%d\n' "$status" | tee -a "$log_file"
exit "$status"
