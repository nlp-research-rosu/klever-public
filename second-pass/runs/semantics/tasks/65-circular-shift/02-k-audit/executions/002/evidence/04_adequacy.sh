#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/reconstruction
evidence=/audit-output/evidence

run_logged() {
  local label=$1
  shift
  echo "\$ $*"
  "$@" 2>&1 | tee "$evidence/$label.log"
  local status=${PIPESTATUS[0]}
  echo "EXIT_STATUS=$status" | tee -a "$evidence/$label.log"
  return "$status"
}

cd "$scratch" || exit 2

run_logged 04a_constructor_compare \
  python3 /audit-output/evidence/04_constructor_compare.py
constructor_status=$?

run_logged 04b_pinning_proof \
  kprove pinning-spec.k \
    --definition audit-verification-kompiled \
    --spec-module AUDIT-PINNING-SPEC \
    --warnings none
pinning_status=$?

echo '$ python3 py2mpy.py adequacy-cases.py > adequacy-cases.mpy'
python3 py2mpy.py adequacy-cases.py > adequacy-cases.mpy
translate_status=$?
echo "EXIT_STATUS=$translate_status"

run_logged 04c_krun_satisfying_cases \
  krun adequacy-cases.mpy \
    --definition audit-runtime-kompiled \
    --output pretty
krun_status=$?

run_logged 04d_python_satisfying_states \
  python3 /audit-output/evidence/04_satisfying_states.py
states_status=$?

run_logged 04e_ground_postcondition \
  kprove ground-spec.k \
    --definition audit-verification-kompiled \
    --spec-module AUDIT-GROUND-SPEC \
    --warnings none
ground_status=$?

run_logged 04f_body_sensitivity \
  kprove body-mutant-spec.k \
    --definition audit-verification-kompiled \
    --spec-module AUDIT-BODY-MUTANT-SPEC \
    --depth 300 \
    --warnings none
body_status=$?

echo "EXPECTED_BODY_MUTATION_FAILURE=$body_status"

if (( constructor_status != 0 || pinning_status != 0 || translate_status != 0 ||
      krun_status != 0 || states_status != 0 )); then
  exit 2
fi

# Ground postcondition closure is informative: it must pass for a direct
# concrete meaning bridge. Body mutation must fail to demonstrate sensitivity.
if (( ground_status != 0 || body_status == 0 )); then
  exit 1
fi
exit 0
