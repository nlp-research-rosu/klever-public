#!/usr/bin/env bash
set -uo pipefail
set -x

work=/tmp/audit-work/rebuild
status=0
cd "$work" || exit 1

python3 -c '
import importlib.util
def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.get_row
canonical = load("/reference/canonical.py", "canonical_false_witness")
generated = load("/candidate/solution.py", "generated_false_witness")
print("false_mutation_witness lst=[] x=7")
print("canonical_result=", canonical([], 7))
print("generated_result=", generated([], 7))
print("mutated_claim_result=", [(0, 0)])
assert canonical([], 7) == generated([], 7) == []
'
rc=$?
printf 'false_mutation_ground_witness_exit=%d\n' "$rc"
(( rc == 0 )) || status=1

kprove spec-vacuity.k \
  --definition audit-verification-kompiled \
  --spec-module AUDIT-SPEC-VACUITY \
  --dry-run
rc=$?
printf 'false_mutation_dry_run_build_exit=%d\n' "$rc"
(( rc == 0 )) || status=1

set +e
kprove spec-vacuity.k \
  --definition audit-verification-kompiled \
  --spec-module AUDIT-SPEC-VACUITY \
  2>&1 | tee /audit-output/evidence/stage6_nonvacuity_proof_output.log
proof_rc=${PIPESTATUS[0]}
set -e
printf 'false_mutation_proof_exit=%d\n' "$proof_rc"
if (( proof_rc == 0 )); then
  status=1
fi

rg -n 'WarnStuckClaimState|implication check|cannot be rewritten further' \
  /audit-output/evidence/stage6_nonvacuity_proof_output.log
residual_rc=$?
printf 'false_mutation_expected_residual_scan_exit=%d\n' "$residual_rc"
(( residual_rc == 0 )) || status=1

printf 'stage6_nonvacuity_exit=%d\n' "$status"
exit "$status"
