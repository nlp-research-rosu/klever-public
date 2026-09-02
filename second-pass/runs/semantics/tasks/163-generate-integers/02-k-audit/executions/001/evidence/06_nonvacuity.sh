#!/usr/bin/env bash
set -u
set -o pipefail

work=/tmp/audit-work/submitted
definition="$work/verification-kompiled"

echo 'CMD: cp reviewer mutation into scratch'
cp /audit-output/evidence/06_spec_vacuity.k "$work/06_spec_vacuity.k"
status=$?
echo "EXIT: $status"
[[ $status -eq 0 ]] || exit "$status"

echo 'CMD: kprove mutation --dry-run (parse/build reachability claim only)'
kprove "$work/06_spec_vacuity.k" \
  --definition "$definition" \
  --spec-module SPEC-VACUITY-AUDIT \
  --dry-run \
  > "$work/06_mutation_dry_run.kore" 2> "$work/06_mutation_dry_run.err"
dry_status=$?
echo "EXIT: $dry_status"
if [[ -s "$work/06_mutation_dry_run.err" ]]; then
  sed -n '1,160p' "$work/06_mutation_dry_run.err"
fi
[[ $dry_status -eq 0 ]] || exit "$dry_status"

echo 'CMD: kprove false-result mutation (expected nonzero stuck obligation)'
kprove "$work/06_spec_vacuity.k" \
  --definition "$definition" \
  --spec-module SPEC-VACUITY-AUDIT \
  --smt-timeout 10000 2>&1 | tee "$work/06_mutation_raw.log"
proof_status=${PIPESTATUS[0]}
echo "EXIT: $proof_status"

echo 'CMD: require expected WarnStuckClaimState/implication failure residual'
rg -n 'WarnStuckClaimState|implication check between the conditions has failed' \
  "$work/06_mutation_raw.log"
residual_status=$?
echo "EXIT: $residual_status"

echo 'CMD: demonstrate concrete satisfying witness and false mutated result'
python3 - "$work" <<'PY'
import importlib.util
import pathlib
import sys

work = pathlib.Path(sys.argv[1])

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.generate_integers

canonical = load(work / "canonical.py", "canonical_mutation")
candidate = load(work / "solution.py", "candidate_mutation")
actual_canonical = canonical(3, 7)
actual_candidate = candidate(3, 7)
mutated_destination = [2, 4, 6]
print("input=(3, 7), precondition=true")
print(f"canonical={actual_canonical}")
print(f"candidate={actual_candidate}")
print(f"false_mutated_destination={mutated_destination}")
print(f"mutation_is_false={actual_candidate != mutated_destination}")
if actual_canonical != [4, 6] or actual_candidate != [4, 6]:
    raise SystemExit(1)
if actual_candidate == mutated_destination:
    raise SystemExit(1)
PY
witness_status=$?
echo "EXIT: $witness_status"

if [[ $proof_status -eq 0 ]]; then
  echo 'ERROR: false mutation unexpectedly proved'
  exit 1
fi
if [[ $residual_status -ne 0 || $witness_status -ne 0 ]]; then
  exit 1
fi
echo 'EXPECTED_FAILURE_CONFIRMED'
exit 0
