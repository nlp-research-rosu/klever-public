#!/usr/bin/env bash
set -uo pipefail

work=/tmp/audit-work/31-is-prime-audit
cd "${work}" || exit 125
failures=0

echo 'MUTATION_FILE: /tmp/audit-work/31-is-prime-audit/spec-vacuity.k'
echo 'FALSE_WITNESS: N=1 satisfies N < 2; canonical.py and solution.py both return False, while the destination demands true.'
sha256sum spec-vacuity.k
nl -ba spec-vacuity.k

echo 'COMMAND (build-only): kprove spec-vacuity.k --definition proof-kompiled --spec-module SPEC-VACUITY --dry-run'
timeout 300 kprove spec-vacuity.k \
  --definition proof-kompiled \
  --spec-module SPEC-VACUITY \
  --dry-run
build_status=$?
echo "EXIT_STATUS (build-only, expected 0): ${build_status}"
if [[ ${build_status} -ne 0 ]]; then failures=$((failures + 1)); fi

echo 'COMMAND (false proof): kprove spec-vacuity.k --definition proof-kompiled --spec-module SPEC-VACUITY'
timeout 900 kprove spec-vacuity.k \
  --definition proof-kompiled \
  --spec-module SPEC-VACUITY
prove_status=$?
echo "EXIT_STATUS (false proof, expected nonzero): ${prove_status}"
if [[ ${prove_status} -eq 0 ]]; then failures=$((failures + 1)); fi

echo 'COMMAND (witness oracle): Python canonical and submitted at N=1'
python3 -c 'import canonical, solution; print("N=1", canonical.is_prime(1), solution.is_prime(1))'
witness_status=$?
echo "EXIT_STATUS (witness oracle): ${witness_status}"
if [[ ${witness_status} -ne 0 ]]; then failures=$((failures + 1)); fi

echo "EXPECTED_MUTATION_FAILURE_OBSERVED: proof_status=${prove_status}"
echo "FAILURE_COUNT: ${failures}"
if [[ ${failures} -ne 0 ]]; then exit 1; fi
exit 0
