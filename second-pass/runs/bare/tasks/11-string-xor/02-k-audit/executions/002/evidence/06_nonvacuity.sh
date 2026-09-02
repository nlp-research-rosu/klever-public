#!/usr/bin/env bash
set -euo pipefail
trap 'rc=$?; echo "EXIT_STATUS=$rc"' EXIT

source_dir=/tmp/audit-work/11-string-xor/source
definition=/tmp/audit-work/11-string-xor/build/verification-kompiled
output=/tmp/audit-work/11-string-xor/nonvacuity.out

echo 'COMMAND: bash /audit-output/evidence/06_nonvacuity.sh'
cd "$source_dir"

echo 'SATISFYING_INPUT: a="0", b="1"; segment encodings (1,seed(0)) and (1,seed(1))'
echo 'TRUE_RESULT: "1" = cons(true,empty)'
echo 'FALSE_MUTATED_OBLIGATION: "0" = cons(false,empty)'

echo 'COMMAND: kprove spec-vacuity-audit.k --dry-run --spec-module XOR-SPEC-VACUITY-AUDIT --definition /tmp/audit-work/11-string-xor/build/verification-kompiled --output pretty'
kprove spec-vacuity-audit.k \
  --dry-run \
  --spec-module XOR-SPEC-VACUITY-AUDIT \
  --definition "$definition" \
  --output pretty
echo 'MUTATION_PARSE_AND_BUILD_EXIT_STATUS=0'

echo 'COMMAND: kprove spec-vacuity-audit.k --spec-module XOR-SPEC-VACUITY-AUDIT --definition /tmp/audit-work/11-string-xor/build/verification-kompiled --output pretty'
set +e
kprove spec-vacuity-audit.k \
  --spec-module XOR-SPEC-VACUITY-AUDIT \
  --definition "$definition" \
  --output pretty \
  > "$output" 2>&1
mutation_status=$?
set -e

cat "$output"
echo "MUTATION_PROOF_EXIT_STATUS=$mutation_status"
test "$mutation_status" -ne 0
grep -F 'WarnStuckClaimState' "$output" > /dev/null
grep -F 'returned ( str ( cons ( true , empty ) ) )' "$output" > /dev/null
echo 'EXPECTED_FALSE_RESULT_OBLIGATION_REJECTED=true'
