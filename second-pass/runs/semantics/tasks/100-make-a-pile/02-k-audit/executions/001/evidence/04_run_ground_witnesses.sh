#!/usr/bin/env bash
set -uo pipefail

cd /tmp/audit-work
cp /audit-output/evidence/04_ground_witness_spec.k ground-witness-spec.k

run_ground() {
  local module=$1
  local log=$2
  (
    printf 'COMMAND: kprove ground-witness-spec.k --definition audit-verification-kompiled --spec-module %s\n' "${module}"
    kprove ground-witness-spec.k \
      --definition audit-verification-kompiled \
      --spec-module "${module}"
    status=$?
    echo "EXIT_STATUS: ${status}"
    exit "${status}"
  ) >"/audit-output/evidence/${log}" 2>&1
}

run_ground PILE-GROUND-ENTRY-SPEC 04a_ground_entry.log
entry_status=$?
run_ground PILE-GROUND-LOOP-WITNESS-SPEC 04b_ground_loop.log
loop_status=$?

echo "ground_entry_status=${entry_status}"
echo "ground_loop_status=${loop_status}"

if (( entry_status != 0 || loop_status != 0 )); then
  exit 1
fi
