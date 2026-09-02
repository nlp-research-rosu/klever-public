#!/usr/bin/env bash
set -u
set -o pipefail

work=/tmp/audit-work
evidence=/audit-output/evidence
failures=0

run_logged() {
  local logfile=$1
  shift
  printf 'COMMAND:' | tee "$logfile"
  printf ' %q' "$@" | tee -a "$logfile"
  printf '\n' | tee -a "$logfile"
  "$@" 2>&1 | tee -a "$logfile"
  local status=${PIPESTATUS[0]}
  printf 'EXIT_STATUS=%s\n' "$status" | tee -a "$logfile"
  return "$status"
}

python3 - <<'PY' | tee "$evidence/stage6_false_witness.log"
import importlib.util

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

canonical = load("canonical", "/reference/canonical.py").prime_fib
generated = load("generated", "/tmp/audit-work/solution.py").prime_fib
print("SATISFYING_INPUT n=1 precondition=(1 > 0)=true")
print(f"canonical(1)={canonical(1)}")
print(f"generated(1)={generated(1)}")
print("mutated_postcondition=result 3")
print(f"demonstrably_false={canonical(1) != 3 and generated(1) != 3}")
PY
witness_status=${PIPESTATUS[0]}
(( witness_status == 0 )) || failures=$((failures + 1))

run_logged "$evidence/stage6_dry_run.log" \
  kprove "$evidence/stage6_spec_vacuity.k" \
    --definition "$work/fresh-verification-kompiled" \
    --spec-module STAGE6-SPEC-VACUITY \
    --claims STAGE6-SPEC-VACUITY.false-result-n1 \
    --dry-run -I "$work" --color off
dry_status=$?
(( dry_status == 0 )) || failures=$((failures + 1))

run_logged "$evidence/stage6_false_proof.log" \
  kprove "$evidence/stage6_spec_vacuity.k" \
    --definition "$work/fresh-verification-kompiled" \
    --spec-module STAGE6-SPEC-VACUITY \
    --claims STAGE6-SPEC-VACUITY.false-result-n1 \
    -I "$work" --color off
proof_status=$?
if (( proof_status == 0 )) || \
   ! grep -q 'WarnStuckClaimState' "$evidence/stage6_false_proof.log"; then
  failures=$((failures + 1))
fi
if grep -qx '#Top' "$evidence/stage6_false_proof.log"; then
  failures=$((failures + 1))
fi

printf 'witness_status=%s\ndry_run_status=%s\nfalse_proof_status=%s\nfailures=%s\n' \
  "$witness_status" "$dry_status" "$proof_status" "$failures"
if (( failures != 0 )); then
  exit 1
fi
printf 'SCRIPT_EXIT=0\n'
