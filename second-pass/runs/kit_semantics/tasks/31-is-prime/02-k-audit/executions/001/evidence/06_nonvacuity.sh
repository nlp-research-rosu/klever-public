#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/prime31
definition="$scratch/reviewer-verification-kompiled"
spec="$scratch/audit-false-result.k"
evidence=/audit-output/evidence

cd "$scratch" || exit 2

echo '$ cmp -s /audit-output/evidence/06_false_result_mutation.k /tmp/audit-work/prime31/audit-false-result.k'
cmp -s "$evidence/06_false_result_mutation.k" "$spec"
copy_status=$?
echo "EXIT: $copy_status"

echo '$ python3 -c <evaluate canonical(31), generated(31)>'
python3 -c 'import importlib.util
def load(name, path):
    s=importlib.util.spec_from_file_location(name, path)
    m=importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m.is_prime
print("canonical(31)=", load("canonical", "/reference/canonical.py")(31))
print("generated(31)=", load("generated", "/tmp/audit-work/prime31/solution.py")(31))' \
  > "$evidence/06_witness_python.log" 2>&1
witness_status=$?
echo "EXIT: $witness_status"
cat "$evidence/06_witness_python.log"

echo '$ kprove audit-false-result.k --definition reviewer-verification-kompiled --spec-module AUDIT-FALSE-RESULT --dry-run'
kprove "$spec" \
  --definition "$definition" \
  --spec-module AUDIT-FALSE-RESULT \
  --dry-run \
  > "$evidence/06_false_dry_run.log" 2>&1
dry_status=$?
echo "EXIT: $dry_status"

echo '$ kprove audit-false-result.k --definition reviewer-verification-kompiled --spec-module AUDIT-FALSE-RESULT'
kprove "$spec" \
  --definition "$definition" \
  --spec-module AUDIT-FALSE-RESULT \
  > "$evidence/06_false_kprove.log" 2>&1
proof_status=$?
echo "EXIT: $proof_status"

if [[ $copy_status -ne 0 || $witness_status -ne 0 || $dry_status -ne 0 ]]; then
  echo 'RESULT=INVALID_TEST_SETUP'
  exit 2
fi
if [[ $proof_status -eq 0 ]]; then
  echo 'RESULT=UNEXPECTED_PROOF_SUCCESS'
  exit 1
fi
if ! grep -q 'WarnStuckClaimState' "$evidence/06_false_kprove.log"; then
  echo 'RESULT=WRONG_FAILURE_MODE'
  exit 3
fi
echo 'RESULT=EXPECTED_UNMET_OBLIGATION'
exit 0
