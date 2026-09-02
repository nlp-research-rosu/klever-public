#!/usr/bin/env bash
set -euo pipefail

scratch=/tmp/audit-work/55-fib-independent-audit
evidence=/audit-output/evidence
cd "$scratch"

printf '%s\n' 'SATISFYING_WITNESS: ARG=2, env=.Map, functions=.Map; Python generated fib(2)=1 and fibMath(2)+1=2'
python3 - <<'PY'
from solution import fib

actual = fib(2)
mutated_target = 2
print(f"generated_fib_2={actual}")
print(f"mutated_target={mutated_target}")
print(f"demonstrably_false={actual != mutated_target}")
assert actual == 1
assert actual != mutated_target
PY

printf '%s\n' 'COMMAND: kprove false-result-spec.k --definition verification-proof-kompiled --spec-module FALSE-RESULT-SPEC --dry-run --output none'
kprove false-result-spec.k \
  --definition verification-proof-kompiled \
  --spec-module FALSE-RESULT-SPEC \
  --dry-run \
  --output none \
  2>&1 | tee "$evidence/06_false_result_dry_run.log"
printf 'EXIT_STATUS false_result_dry_run=0 BUILD_SUCCESS=true\n'

printf '%s\n' 'COMMAND: kprove false-result-spec.k --definition verification-proof-kompiled --spec-module FALSE-RESULT-SPEC --output pretty'
set +e
kprove false-result-spec.k \
  --definition verification-proof-kompiled \
  --spec-module FALSE-RESULT-SPEC \
  --output pretty \
  > "$evidence/06_false_result_proof.log" 2>&1
proof_status=$?
set -e
sed -n '1,180p' "$evidence/06_false_result_proof.log"
printf 'EXIT_STATUS false_result_proof=%s EXPECTED_NONZERO=true\n' "$proof_status"
test "$proof_status" -ne 0
grep -q 'WarnStuckClaimState' "$evidence/06_false_result_proof.log"
grep -q 'cannot be rewritten further' "$evidence/06_false_result_proof.log"
