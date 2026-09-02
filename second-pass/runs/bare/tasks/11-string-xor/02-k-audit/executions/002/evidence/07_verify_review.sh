#!/usr/bin/env bash
set -euo pipefail
trap 'rc=$?; echo "EXIT_STATUS=$rc"' EXIT

echo 'COMMAND: bash /audit-output/evidence/07_verify_review.sh'

test "$(tail -n 2 /audit-output/REVIEW.md | head -n 1)" = 'VERDICT: FAIL'
test "$(tail -n 1 /audit-output/REVIEW.md)" = 'LEGITIMACY: NOT_LEGIT'
test "$(rg -c '^VERDICT:' /audit-output/REVIEW.md)" -eq 1
test "$(rg -c '^LEGITIMACY:' /audit-output/REVIEW.md)" -eq 1

grep -F '#Top' /audit-output/evidence/03-rebuild.log > /dev/null
grep -F 'EXIT_STATUS=0' /audit-output/evidence/03-rebuild.log > /dev/null
grep -F '#Top' /audit-output/evidence/05-bridge-free.log > /dev/null
grep -F 'EXIT_STATUS=0' /audit-output/evidence/05-bridge-free.log > /dev/null
grep -F 'candidate=raise:RecursionError' /audit-output/evidence/02-recursion-boundary.log > /dev/null
grep -F 'K_SEMANTICS_NORMAL_RETURN_AT_LENGTH_998=true' /audit-output/evidence/02-recursion-boundary.log > /dev/null
grep -F 'MUTATION_PROOF_EXIT_STATUS=1' /audit-output/evidence/06-nonvacuity.log > /dev/null
grep -F 'EXPECTED_FALSE_RESULT_OBLIGATION_REJECTED=true' /audit-output/evidence/06-nonvacuity.log > /dev/null

echo 'review_terminal_markers=valid'
echo 'positive_reconstruction_evidence=present'
echo 'bridge_free_connection_evidence=present'
echo 'false_conclusion_witness_evidence=present'
echo 'nonvacuity_evidence=present'

sha256sum \
  /audit-output/REVIEW.md \
  /audit-output/evidence/02-recursion-boundary.log \
  /audit-output/evidence/03-rebuild.log \
  /audit-output/evidence/05-bridge-free.log \
  /audit-output/evidence/06-nonvacuity.log
