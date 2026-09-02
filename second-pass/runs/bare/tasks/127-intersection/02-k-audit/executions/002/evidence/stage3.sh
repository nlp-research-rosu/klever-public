#!/usr/bin/env bash
set -u

source_dir=/tmp/audit-work/candidate-src
concrete_definition=/tmp/audit-work/build-concrete/semantic-v2-kompiled
loop_definition=/tmp/audit-work/build-proof/loop-v2-kompiled
whole_definition=/tmp/audit-work/build-proof/verification-v2-kompiled
evidence_dir=/audit-output/evidence

cd "${source_dir}" || exit 90

echo "COMMAND: kompile semantic.k --main-module MPY --syntax-module MPY-SYNTAX --backend llvm --output-definition ${concrete_definition}"
kompile semantic.k \
  --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --backend llvm \
  --output-definition "${concrete_definition}" \
  > "${evidence_dir}/kompile-concrete.log" 2>&1
concrete_build_status=$?
echo "EXIT: ${concrete_build_status}"
sed -n '1,180p' "${evidence_dir}/kompile-concrete.log"

echo 'COMMAND: python3 /audit-output/evidence/semantics_differential.py'
python3 "${evidence_dir}/semantics_differential.py" \
  > "${evidence_dir}/semantics-differential.log" 2>&1
semantics_status=$?
echo "EXIT: ${semantics_status}"
sed -n '1,260p' "${evidence_dir}/semantics-differential.log"

echo "COMMAND: kompile verification.k --main-module VERIFICATION --syntax-module MPY-SYNTAX --backend haskell --output-definition ${loop_definition}"
kompile verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --backend haskell \
  --output-definition "${loop_definition}" \
  > "${evidence_dir}/kompile-loop.log" 2>&1
loop_build_status=$?
echo "EXIT: ${loop_build_status}"
sed -n '1,180p' "${evidence_dir}/kompile-loop.log"

echo "COMMAND: kprove spec.k --definition ${loop_definition} --spec-module LOOP-CORRECTNESS-SPEC --output pretty"
kprove spec.k \
  --definition "${loop_definition}" \
  --spec-module LOOP-CORRECTNESS-SPEC \
  --output pretty \
  > "${evidence_dir}/kprove-loop.log" 2>&1
loop_proof_status=$?
loop_top_count=$(rg -c '^#Top$' "${evidence_dir}/kprove-loop.log" || true)
echo "EXIT: ${loop_proof_status}"
echo "TOP_COUNT: ${loop_top_count}"
sed -n '1,220p' "${evidence_dir}/kprove-loop.log"

echo "COMMAND: kompile verification.k --main-module VERIFICATION-WITH-LOOP-LEMMA --syntax-module MPY-SYNTAX --backend haskell --output-definition ${whole_definition}"
kompile verification.k \
  --main-module VERIFICATION-WITH-LOOP-LEMMA \
  --syntax-module MPY-SYNTAX \
  --backend haskell \
  --output-definition "${whole_definition}" \
  > "${evidence_dir}/kompile-whole.log" 2>&1
whole_build_status=$?
echo "EXIT: ${whole_build_status}"
sed -n '1,180p' "${evidence_dir}/kompile-whole.log"

echo "COMMAND: kprove spec.k --definition ${whole_definition} --spec-module SPEC --output pretty"
kprove spec.k \
  --definition "${whole_definition}" \
  --spec-module SPEC \
  --output pretty \
  > "${evidence_dir}/kprove-whole.log" 2>&1
whole_proof_status=$?
whole_top_count=$(rg -c '^#Top$' "${evidence_dir}/kprove-whole.log" || true)
echo "EXIT: ${whole_proof_status}"
echo "TOP_COUNT: ${whole_top_count}"
sed -n '1,220p' "${evidence_dir}/kprove-whole.log"

if [ "${concrete_build_status}" -ne 0 ] \
   || [ "${semantics_status}" -ne 0 ] \
   || [ "${loop_build_status}" -ne 0 ] \
   || [ "${loop_proof_status}" -ne 0 ] \
   || [ "${loop_top_count}" != "1" ] \
   || [ "${whole_build_status}" -ne 0 ] \
   || [ "${whole_proof_status}" -ne 0 ] \
   || [ "${whole_top_count}" != "1" ]; then
  exit 1
fi
