#!/usr/bin/env bash
set -u

SCRATCH=/tmp/audit-work/body-sensitivity
MUT_DEF="$SCRATCH/verification-mut-haskell"
CONCRETE_DEF=/tmp/audit-work/reconstruction/semantic-llvm

run_shell() {
  local command_text="$1"
  printf 'COMMAND: %s\n' "$command_text"
  bash -o pipefail -c "$command_text"
  local status=$?
  printf 'EXIT_STATUS: %s\n\n' "$status"
  return "$status"
}

run_shell "mkdir -p '$SCRATCH'"
run_shell "cp /tmp/audit-work/source/semantic.k '$SCRATCH/semantic.k'"
run_shell "cp /tmp/audit-work/source/spec.k '$SCRATCH/spec.k'"
run_shell "cp /audit-output/evidence/stage5/verification-body-mut.k '$SCRATCH/verification.k'"
run_shell "cp /audit-output/evidence/stage5/solution-body-mut.py '$SCRATCH/solution-body-mut.py'"
run_shell "python3 /reference/py2mpy.py '$SCRATCH/solution-body-mut.py' > '$SCRATCH/solution-body-mut.mpy'"

printf 'CONCRETE FALSE WITNESS FOR THE BODY MUTATION (N=78)\n'
run_shell "krun '$SCRATCH/solution-body-mut.mpy' -cN=78 --definition '$CONCRETE_DEF'"
concrete_status=$?
run_shell "python3 -c \"import importlib.util; p=importlib.util.spec_from_file_location('m','$SCRATCH/solution-body-mut.py'); m=importlib.util.module_from_spec(p); p.loader.exec_module(m); print('MUTATED_PYTHON:',m.fizz_buzz(78))\""
mut_python_status=$?
run_shell "python3 /audit-output/evidence/stage3/compare_concrete.py 78"
oracle_status=$?

printf 'MUTATED PROOF DEFINITION BUILD\n'
run_shell "cd '$SCRATCH' && kompile verification.k --main-module VERIFICATION --syntax-module MPY-SYNTAX --backend haskell --output-definition '$MUT_DEF'"
build_status=$?
if [[ $build_status -ne 0 ]]; then
  exit 1
fi

printf 'EXPECTED FAILURE: BODY NOW ADDS TWO BUT SUMMARY STILL COUNTS ONE\n'
command_text="cd '$SCRATCH' && timeout 60s kprove spec.k --definition '$MUT_DEF' --spec-module SPEC"
printf 'COMMAND: %s\n' "$command_text"
proof_output=$(bash -o pipefail -c "$command_text" 2>&1)
proof_status=$?
printf '%s\n' "$proof_output"
printf 'EXIT_STATUS: %s\n' "$proof_status"
if printf '%s\n' "$proof_output" | rg -q 'WarnStuckClaimState'; then
  expected_residual=0
else
  expected_residual=1
fi
printf 'EXPECTED_STUCK_RESIDUAL_PRESENT: %s\n' "$((1 - expected_residual))"
printf 'SUMMARY concrete=%s mut_python=%s oracle=%s build=%s proof=%s residual_check=%s\n' \
  "$concrete_status" "$mut_python_status" "$oracle_status" "$build_status" "$proof_status" "$expected_residual"

if [[ $concrete_status -ne 0 || $mut_python_status -ne 0 || $oracle_status -ne 0 || $proof_status -eq 0 || $proof_status -eq 124 || $expected_residual -ne 0 ]]; then
  exit 1
fi
exit 0

