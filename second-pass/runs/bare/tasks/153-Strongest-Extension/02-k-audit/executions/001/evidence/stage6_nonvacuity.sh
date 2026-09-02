#!/usr/bin/env bash
set -u
status=0

spec=/tmp/audit-work/candidate-src/spec-vacuity-auditor.k
proof_def=/tmp/audit-work/verification-kompiled-fresh
raw_log=/audit-output/evidence/stage6_mutation_proof.raw.log

echo '$ witness ground truth: canonical and candidate return C.Zz'
python3 - <<'PY'
import importlib.util

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.Strongest_Extension

canonical = load("/reference/canonical.py", "canonical_vacuity")
candidate = load("/tmp/audit-work/candidate-src/solution.py", "candidate_vacuity")
assert canonical("C", ["Zz"]) == "C.Zz"
assert candidate("C", ["Zz"]) == "C.Zz"
print('canonical_result="C.Zz"')
print('candidate_result="C.Zz"')
print('mutated_claim_result="C.WRONG"')
PY
rc=$?
echo "ground_truth_exit=$rc"
(( rc == 0 )) || status=1

echo '$ kprove mutation --dry-run (parse/build check)'
kprove "$spec" --definition "$proof_def" \
  --spec-module SPEC-VACUITY-AUDITOR --dry-run
dry_rc=$?
echo "dry_run_exit=$dry_rc"
(( dry_rc == 0 )) || status=1

echo '$ kprove fresh false result mutation (expected proof failure)'
kprove "$spec" --definition "$proof_def" \
  --spec-module SPEC-VACUITY-AUDITOR 2>&1 | tee "$raw_log"
proof_rc=${PIPESTATUS[0]}
echo "mutation_proof_exit=$proof_rc"
if (( proof_rc == 0 )); then
  status=1
fi

echo '$ require expected unmet-obligation diagnostic'
rg -n 'WarnStuckClaimState|implication check.*failed|cannot be rewritten further' "$raw_log"
diagnostic_rc=$?
echo "diagnostic_check_exit=$diagnostic_rc"
(( diagnostic_rc == 0 )) || status=1

echo "stage6_exit=$status"
exit "$status"
