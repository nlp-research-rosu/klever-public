#!/usr/bin/env bash
set -uo pipefail

cd /tmp/audit-work/58-common
cp /audit-output/evidence/mutated-program.mpy mutated-program.mpy
cp /audit-output/evidence/spec-body-sensitivity-audit.k spec-body-sensitivity-audit.k

echo 'COMMAND: kast mutated-program.mpy --definition verification-audit-kompiled --module VERIFICATION --sort Module --expand-macros --output json --output-file mutated-expanded.json'
kast mutated-program.mpy \
  --definition verification-audit-kompiled \
  --module VERIFICATION \
  --sort Module \
  --expand-macros \
  --output json \
  --output-file mutated-expanded.json
kast_status=$?
echo "EXIT: ${kast_status}"

echo 'COMMAND: cmp -s solution-expanded.json mutated-expanded.json'
cmp -s solution-expanded.json mutated-expanded.json
cmp_status=$?
echo "EXIT: ${cmp_status}"
sha256sum solution-expanded.json mutated-expanded.json
if [[ ${cmp_status} -ne 0 ]]; then
  echo 'MUTATED_PROGRAM_TERM_DIFFERS: yes'
else
  echo 'MUTATED_PROGRAM_TERM_DIFFERS: no'
fi

echo 'COMMAND: kprove spec-body-sensitivity-audit.k --definition verification-audit-kompiled --spec-module SPEC-BODY-SENSITIVITY-AUDIT'
kprove spec-body-sensitivity-audit.k \
  --definition verification-audit-kompiled \
  --spec-module SPEC-BODY-SENSITIVITY-AUDIT \
  2>&1 | tee body-sensitivity-raw.log
proof_status=${PIPESTATUS[0]}
echo "KPROVE_EXIT: ${proof_status}"

rg -q 'WarnStuckClaimState' body-sensitivity-raw.log
stuck_status=$?
rg -q '0 \|-> list \( \.ValSeq \)' body-sensitivity-raw.log
empty_actual_status=$?
echo "WARN_STUCK_PRESENT: $([[ ${stuck_status} -eq 0 ]] && echo yes || echo no)"
echo "EMPTY_MUTANT_RESULT_PRESENT: $([[ ${empty_actual_status} -eq 0 ]] && echo yes || echo no)"

if [[ ${kast_status} -ne 0 || ${cmp_status} -eq 0 || ${proof_status} -eq 0 || ${stuck_status} -ne 0 || ${empty_actual_status} -ne 0 ]]; then
  exit 1
fi
echo 'BODY_SENSITIVITY_RESULT: changed executed term invalidates original result'
