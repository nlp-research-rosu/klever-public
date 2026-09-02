#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/140-fix-spaces/source
cd "$scratch" || exit 90
failures=0

echo '$ show the fresh false mutation and its empty-input witness'
nl -ba spec-vacuity.k
python3 - <<'PY'
import importlib.util

spec = importlib.util.spec_from_file_location("candidate_empty_witness", "solution.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
actual = module.fix_spaces("")
mutated = actual + "!"
print("satisfying_input=''")
print("actual_result=", repr(actual))
print("mutated_required_result=", repr(mutated))
assert actual == ""
assert mutated == "!"
PY
witness_status=$?
echo "exit=$witness_status"

echo '$ dry-run the mutation to require successful parsing and KORE construction'
kprove spec-vacuity.k \
  --definition fresh-proof-main-kompiled \
  --spec-module SPEC-VACUITY \
  --dry-run \
  --output-file /audit-output/evidence/spec-vacuity.kore
dry_status=$?
echo "exit=$dry_status"

echo '$ run the fresh false mutation; a stuck implication is expected'
kprove spec-vacuity.k \
  --definition fresh-proof-main-kompiled \
  --spec-module SPEC-VACUITY
proof_status=$?
echo "exit=$proof_status (nonzero expected)"

if [ "$witness_status" -ne 0 ] ||
   [ "$dry_status" -ne 0 ] ||
   [ "$proof_status" -eq 0 ]; then
  failures=1
fi

echo "audit_check_failures=$failures"
exit "$failures"
