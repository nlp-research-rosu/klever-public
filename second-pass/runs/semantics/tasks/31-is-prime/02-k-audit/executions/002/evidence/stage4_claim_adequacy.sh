#!/usr/bin/env bash
set -uo pipefail

work=/tmp/audit-work/31-is-prime-audit
echo 'COMMAND: python3 claim_witnesses.py'
python3 /audit-output/evidence/claim_witnesses.py
witness_status=$?
echo "EXIT_STATUS: ${witness_status}"

echo 'COMMAND: rg -n isPrimeSpec|trialPrime spec.k verification.k'
rg -n 'isPrimeSpec|trialPrime' "${work}/spec.k" "${work}/verification.k"
search_status=$?
echo "EXIT_STATUS: ${search_status}"

echo 'COMMAND: rg -n claims and k-cell destinations in spec.k'
rg -n 'claim|=>|trialPrime|isPrimeSpec|Return[(]Bool' "${work}/spec.k"
claim_status=$?
echo "EXIT_STATUS: ${claim_status}"

if [[ ${witness_status} -ne 0 || ${search_status} -ne 0 || ${claim_status} -ne 0 ]]; then
  exit 1
fi
exit 0
