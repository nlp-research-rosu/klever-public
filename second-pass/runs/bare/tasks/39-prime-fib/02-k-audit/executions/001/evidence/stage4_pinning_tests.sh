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

cd "$work" || exit 99

# Actual fixed semantics contradicts the summary claim's empty final env.
run_logged "$evidence/stage4_no_summary_empty_env.log" \
  kprove "$evidence/stage4_no_summary_empty_env.k" \
    --definition "$work/fresh-concrete-kompiled" \
    --spec-module STAGE4-NO-SUMMARY-EMPTY-ENV \
    --claims STAGE4-NO-SUMMARY-EMPTY-ENV.actual-program-does-not-preserve-empty-env \
    -I "$work" --color off
no_summary_status=$?
if (( no_summary_status == 0 )) || \
   ! grep -q 'WarnStuckClaimState' "$evidence/stage4_no_summary_empty_env.log"; then
  failures=$((failures + 1))
fi

# The mutated body concretely returns 999 under the generated semantics.
run_logged "$evidence/stage4_body_mutated_krun.log" \
  krun "$evidence/stage4_body_mutated_solution.mpy" \
    --definition "$work/fresh-semantic-kompiled" \
    -cN=1 --output pretty
mutated_krun_status=$?
mutated_result=$(awk '
  /^[[:space:]]*<result>[[:space:]]*$/ {
    getline
    gsub(/[[:space:]]/, "")
    print
    exit
  }
' "$evidence/stage4_body_mutated_krun.log")
printf 'MUTATED_FIXED_RESULT=%s\n' "$mutated_result" \
  | tee -a "$evidence/stage4_body_mutated_krun.log"
if (( mutated_krun_status != 0 )) || [[ "$mutated_result" != 999 ]]; then
  failures=$((failures + 1))
fi

run_logged "$evidence/stage4_body_mutated_build.log" \
  kompile --backend haskell \
    "$evidence/stage4_body_mutated_verification.k" \
    --main-module VERIFICATION \
    --syntax-module MPY-SYNTAX \
    --output-definition "$work/fresh-body-mutated-kompiled" \
    -I "$work"
mutated_build_status=$?
if (( mutated_build_status != 0 )); then
  failures=$((failures + 1))
else
  run_logged "$evidence/stage4_body_mutated_proof.log" \
    kprove "$evidence/stage4_body_mutated_spec.k" \
      --definition "$work/fresh-body-mutated-kompiled" \
      --spec-module STAGE4-BODY-MUTATED-SPEC \
      --claims STAGE4-BODY-MUTATED-SPEC.body-sensitivity-n1 \
      -I "$work" -I "$evidence" --color off
  mutated_proof_status=$?
  # Closure here is the expected witness of body insensitivity.
  if (( mutated_proof_status != 0 )) || \
     ! grep -qx '#Top' "$evidence/stage4_body_mutated_proof.log"; then
    failures=$((failures + 1))
  fi
fi

# Ground substitutions of the general postcondition agree at the value level.
for item in n1 n4 n6; do
  run_logged "$evidence/stage4_ground_${item}.log" \
    kprove "$evidence/stage4_ground_spec.k" \
      --definition "$work/fresh-verification-kompiled" \
      --spec-module STAGE4-GROUND-SPEC \
      --claims "STAGE4-GROUND-SPEC.substitute-${item}" \
      -I "$work" --color off
  status=$?
  if (( status != 0 )) || ! grep -qx '#Top' "$evidence/stage4_ground_${item}.log"; then
    failures=$((failures + 1))
  fi
done

python3 - <<'PY'
import importlib.util

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

canonical = load("canonical", "/reference/canonical.py").prime_fib
generated = load("generated", "/tmp/audit-work/solution.py").prime_fib
for n, claimed in [(1, 2), (4, 13), (6, 233)]:
    c = canonical(n)
    g = generated(n)
    print(f"GROUND n={n} claimed={claimed} canonical={c} generated={g} "
          f"match={claimed == c == g}")
PY
python_compare_status=$?
(( python_compare_status == 0 )) || failures=$((failures + 1))

printf 'no_summary_status=%s\nmutated_krun_status=%s\nmutated_build_status=%s\nfailures=%s\n' \
  "$no_summary_status" "$mutated_krun_status" "$mutated_build_status" "$failures"
if (( failures != 0 )); then
  exit 1
fi
printf 'SCRIPT_EXIT=0\n'
