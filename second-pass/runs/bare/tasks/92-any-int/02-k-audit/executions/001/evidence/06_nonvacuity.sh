#!/usr/bin/env bash
set -u

work=/tmp/audit-work/92-any-int
spec="$work/src/spec-vacuity-audit.k"
definition="$work/proof-kompiled"
log=/audit-output/evidence/06_nonvacuity.log
exec > >(tee "$log") 2>&1

run() {
  printf '\nCOMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf 'EXIT_STATUS: %d\n' "$status"
  return "$status"
}

printf 'AUDIT_STAGE: 6 fresh non-vacuity mutation\n'
printf 'SATISFYING_WITNESS: X=1, Y=2, Z=3; 1 + 2 == 3\n'

run krun -d /tmp/audit-work/92-any-int/concrete-kompiled \
  '-cPGM=RunAnyInt(intVal(1), intVal(2), intVal(3))'
witness_status=$?

run python3 -c 'import importlib.util; p="/tmp/audit-work/92-any-int/src/solution.py"; s=importlib.util.spec_from_file_location("mut_witness",p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); print(m.any_int(1,2,3)); raise SystemExit(0 if m.any_int(1,2,3) is True else 1)'
python_status=$?

run kprove "$spec" \
  --definition "$definition" \
  --spec-module ANY-INT-SPEC-VACUITY-AUDIT \
  --dry-run
dry_status=$?

failure_output="$work/generated/nonvacuity-proof-output.txt"
printf '\nCOMMAND: kprove %q --definition %q --spec-module ANY-INT-SPEC-VACUITY-AUDIT\n' "$spec" "$definition"
kprove "$spec" \
  --definition "$definition" \
  --spec-module ANY-INT-SPEC-VACUITY-AUDIT \
  2>&1 | tee "$failure_output"
prove_status=${PIPESTATUS[0]}
printf 'EXIT_STATUS: %d\n' "$prove_status"

if rg -q 'WarnStuckClaimState' "$failure_output"; then
  printf 'EXPECTED_STUCK_RESIDUAL: present\n'
  residual_status=0
else
  printf 'EXPECTED_STUCK_RESIDUAL: missing\n'
  residual_status=1
fi

if rg -q 'boolVal[^[:alnum:]]*true|true.*#Equals.*false|false.*#Equals.*true' "$failure_output"; then
  printf 'EXPECTED_FALSE_RESULT_CONFLICT: visible\n'
  conflict_status=0
else
  printf 'EXPECTED_FALSE_RESULT_CONFLICT: inspect residual above\n'
  conflict_status=1
fi

if [ "$witness_status" -eq 0 ] \
   && [ "$python_status" -eq 0 ] \
   && [ "$dry_status" -eq 0 ] \
   && [ "$prove_status" -ne 0 ] \
   && [ "$residual_status" -eq 0 ] \
   && [ "$conflict_status" -eq 0 ]; then
  printf 'NONVACUITY_RESULT: PASS\n'
  exit 0
fi

printf 'NONVACUITY_RESULT: FAIL\n'
exit 1
