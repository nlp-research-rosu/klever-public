#!/usr/bin/env bash
set -uo pipefail

cd /tmp/audit-work/58-common
cp /audit-output/evidence/claim-program.mpy claim-program.mpy
cp /audit-output/evidence/spec-ground.k spec-ground.k

echo 'COMMAND: kast solution.mpy --definition verification-audit-kompiled --module VERIFICATION --sort Module --expand-macros --output json --output-file solution-expanded.json'
kast solution.mpy \
  --definition verification-audit-kompiled \
  --module VERIFICATION \
  --sort Module \
  --expand-macros \
  --output json \
  --output-file solution-expanded.json
solution_kast_status=$?
echo "EXIT: ${solution_kast_status}"

echo 'COMMAND: kast claim-program.mpy --definition verification-audit-kompiled --module VERIFICATION --sort Module --expand-macros --output json --output-file claim-expanded.json'
kast claim-program.mpy \
  --definition verification-audit-kompiled \
  --module VERIFICATION \
  --sort Module \
  --expand-macros \
  --output json \
  --output-file claim-expanded.json
claim_kast_status=$?
echo "EXIT: ${claim_kast_status}"

echo 'COMMAND: cmp -s solution-expanded.json claim-expanded.json'
cmp -s solution-expanded.json claim-expanded.json
constructor_cmp_status=$?
echo "EXIT: ${constructor_cmp_status}"
sha256sum solution-expanded.json claim-expanded.json
if [[ ${constructor_cmp_status} -eq 0 ]]; then
  echo 'CONSTRUCTOR_LEVEL_IDENTITY: yes'
else
  echo 'CONSTRUCTOR_LEVEL_IDENTITY: no'
  diff -u solution-expanded.json claim-expanded.json
fi

echo 'COMMAND: kprove spec-ground.k --definition verification-audit-kompiled --spec-module SPEC-GROUND'
kprove spec-ground.k \
  --definition verification-audit-kompiled \
  --spec-module SPEC-GROUND
ground_proof_status=$?
echo "EXIT: ${ground_proof_status}"

echo 'COMMAND: Python canonical/common and generated/common on [1], [1]'
python3 - <<'PY'
from canonical import common as canonical_common
from solution import common as generated_common

left = [1]
right = [1]
print(f"input_left={left!r} input_right={right!r}")
print(f"canonical_result={canonical_common(left, right)!r}")
print(f"generated_result={generated_common(left, right)!r}")
assert canonical_common(left, right) == [1]
assert generated_common(left, right) == [1]
PY
python_status=$?
echo "EXIT: ${python_status}"

if [[ ${solution_kast_status} -ne 0 || ${claim_kast_status} -ne 0 || ${constructor_cmp_status} -ne 0 || ${ground_proof_status} -ne 0 || ${python_status} -ne 0 ]]; then
  exit 1
fi
