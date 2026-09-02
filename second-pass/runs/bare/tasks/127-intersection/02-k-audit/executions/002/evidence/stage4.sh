#!/usr/bin/env bash
set -u

source_dir=/tmp/audit-work/candidate-src
mutation_dir=/tmp/audit-work/mutations
loop_definition=/tmp/audit-work/build-proof/loop-kompiled
whole_definition=/tmp/audit-work/build-proof/verification-kompiled
body_definition=/tmp/audit-work/build-proof/body-mutation-v3-kompiled
evidence_dir=/audit-output/evidence

echo "COMMAND: python3 ${evidence_dir}/make_program_checks.py pin > ${source_dir}/pin-check.k"
python3 "${evidence_dir}/make_program_checks.py" pin > "${source_dir}/pin-check.k"
pin_generation_status=$?
echo "EXIT: ${pin_generation_status}"

echo "COMMAND: kprove pin-check.k --definition ${loop_definition} --spec-module PIN-CHECK-SPEC --output pretty"
cd "${source_dir}" || exit 90
kprove pin-check.k \
  --definition "${loop_definition}" \
  --spec-module PIN-CHECK-SPEC \
  --output pretty \
  > "${evidence_dir}/pin-check.log" 2>&1
pin_status=$?
pin_top_count=$(rg -c '^#Top$' "${evidence_dir}/pin-check.log" || true)
echo "EXIT: ${pin_status}"
echo "TOP_COUNT: ${pin_top_count}"
sed -n '1,180p' "${evidence_dir}/pin-check.log"

echo "COMMAND: cp ${evidence_dir}/fixed-state-witness.k ${source_dir}/fixed-state-witness.k"
cp "${evidence_dir}/fixed-state-witness.k" "${source_dir}/fixed-state-witness.k"
fixed_copy_status=$?
echo "EXIT: ${fixed_copy_status}"

echo "COMMAND: kprove fixed-state-witness.k --definition ${loop_definition} --spec-module FIXED-STATE-WITNESS-SPEC --output pretty"
kprove fixed-state-witness.k \
  --definition "${loop_definition}" \
  --spec-module FIXED-STATE-WITNESS-SPEC \
  --output pretty \
  > "${evidence_dir}/fixed-state-witness.log" 2>&1
fixed_status=$?
fixed_stuck_count=$(rg -c 'WarnStuckClaimState' "${evidence_dir}/fixed-state-witness.log" || true)
echo "EXIT: ${fixed_status} (expected nonzero)"
echo "STUCK_COUNT: ${fixed_stuck_count}"
sed -n '1,260p' "${evidence_dir}/fixed-state-witness.log"

echo "COMMAND: cp ${evidence_dir}/bridge-state-witness.k ${source_dir}/bridge-state-witness.k"
cp "${evidence_dir}/bridge-state-witness.k" "${source_dir}/bridge-state-witness.k"
bridge_copy_status=$?
echo "EXIT: ${bridge_copy_status}"

echo "COMMAND: kprove bridge-state-witness.k --definition ${whole_definition} --spec-module BRIDGE-STATE-WITNESS-SPEC --output pretty"
kprove bridge-state-witness.k \
  --definition "${whole_definition}" \
  --spec-module BRIDGE-STATE-WITNESS-SPEC \
  --output pretty \
  > "${evidence_dir}/bridge-state-witness.log" 2>&1
bridge_status=$?
bridge_top_count=$(rg -c '^#Top$' "${evidence_dir}/bridge-state-witness.log" || true)
echo "EXIT: ${bridge_status}"
echo "TOP_COUNT: ${bridge_top_count}"
sed -n '1,180p' "${evidence_dir}/bridge-state-witness.log"

echo "COMMAND: python3 ${evidence_dir}/make_program_checks.py body-definition > ${source_dir}/verification-body-mutation.k"
python3 "${evidence_dir}/make_program_checks.py" body-definition \
  > "${source_dir}/verification-body-mutation.k"
body_definition_generation_status=$?
echo "EXIT: ${body_definition_generation_status}"

echo "COMMAND: python3 ${evidence_dir}/make_program_checks.py body-spec > ${source_dir}/spec-body-mutation.k"
python3 "${evidence_dir}/make_program_checks.py" body-spec \
  > "${source_dir}/spec-body-mutation.k"
body_spec_generation_status=$?
echo "EXIT: ${body_spec_generation_status}"

echo "COMMAND: kompile verification-body-mutation.k --main-module BODY-MUTATION --syntax-module MPY-SYNTAX --backend haskell --output-definition ${body_definition}"
kompile verification-body-mutation.k \
  --main-module BODY-MUTATION \
  --syntax-module MPY-SYNTAX \
  --backend haskell \
  --output-definition "${body_definition}" \
  > "${evidence_dir}/kompile-body-mutation.log" 2>&1
body_build_status=$?
echo "EXIT: ${body_build_status}"
sed -n '1,180p' "${evidence_dir}/kompile-body-mutation.log"

echo "COMMAND: kprove spec-body-mutation.k --definition ${body_definition} --spec-module BODY-MUTATION-SPEC --output pretty"
kprove spec-body-mutation.k \
  --definition "${body_definition}" \
  --spec-module BODY-MUTATION-SPEC \
  --output pretty \
  > "${evidence_dir}/body-mutation.log" 2>&1
body_proof_status=$?
body_stuck_count=$(rg -c 'WarnStuckClaimState' "${evidence_dir}/body-mutation.log" || true)
echo "EXIT: ${body_proof_status} (expected nonzero)"
echo "STUCK_COUNT: ${body_stuck_count}"
sed -n '1,280p' "${evidence_dir}/body-mutation.log"

if [ "${pin_generation_status}" -ne 0 ] \
   || [ "${pin_status}" -ne 0 ] \
   || [ "${pin_top_count}" != "1" ] \
   || [ "${fixed_copy_status}" -ne 0 ] \
   || [ "${fixed_status}" -eq 0 ] \
   || [ "${fixed_stuck_count}" -lt 1 ] \
   || [ "${bridge_copy_status}" -ne 0 ] \
   || [ "${bridge_status}" -ne 0 ] \
   || [ "${bridge_top_count}" != "1" ] \
   || [ "${body_definition_generation_status}" -ne 0 ] \
   || [ "${body_spec_generation_status}" -ne 0 ] \
   || [ "${body_build_status}" -ne 0 ] \
   || [ "${body_proof_status}" -eq 0 ] \
   || [ "${body_stuck_count}" -lt 1 ]; then
  exit 1
fi
