#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/reconstruction
cd "$scratch" || exit 90

echo "COMMAND python3 /audit-output/evidence/04_extract_claim_program.py 0 > claim-program-odd.mpy"
python3 /audit-output/evidence/04_extract_claim_program.py 0 > claim-program-odd.mpy
odd_extract_status=$?
echo "ODD_EXTRACT_EXIT=$odd_extract_status"

echo "COMMAND python3 /audit-output/evidence/04_extract_claim_program.py 1 > claim-program-even.mpy"
python3 /audit-output/evidence/04_extract_claim_program.py 1 > claim-program-even.mpy
even_extract_status=$?
echo "EVEN_EXTRACT_EXIT=$even_extract_status"

echo "COMMAND kast solution.mpy --definition verification-kompiled --sort Module --output kore > solution.kore"
kast solution.mpy \
  --definition verification-kompiled \
  --sort Module \
  --output kore > solution.kore
solution_parse_status=$?
echo "SOLUTION_PARSE_EXIT=$solution_parse_status"

echo "COMMAND kast claim-program-odd.mpy --definition verification-kompiled --sort Module --output kore > claim-program-odd.kore"
kast claim-program-odd.mpy \
  --definition verification-kompiled \
  --sort Module \
  --output kore > claim-program-odd.kore
odd_parse_status=$?
echo "ODD_PARSE_EXIT=$odd_parse_status"

echo "COMMAND kast claim-program-even.mpy --definition verification-kompiled --sort Module --output kore > claim-program-even.kore"
kast claim-program-even.mpy \
  --definition verification-kompiled \
  --sort Module \
  --output kore > claim-program-even.kore
even_parse_status=$?
echo "EVEN_PARSE_EXIT=$even_parse_status"

echo "COMMAND cmp -s solution.kore claim-program-odd.kore"
cmp -s solution.kore claim-program-odd.kore
odd_cmp_status=$?
echo "ODD_CONSTRUCTOR_CMP_EXIT=$odd_cmp_status"

echo "COMMAND cmp -s solution.kore claim-program-even.kore"
cmp -s solution.kore claim-program-even.kore
even_cmp_status=$?
echo "EVEN_CONSTRUCTOR_CMP_EXIT=$even_cmp_status"

echo "COMMAND sha256sum solution.kore claim-program-odd.kore claim-program-even.kore"
sha256sum solution.kore claim-program-odd.kore claim-program-even.kore
hash_status=$?
echo "KORE_HASH_EXIT=$hash_status"

echo "COMMAND python3 /audit-output/evidence/04_ground_claims.py"
python3 /audit-output/evidence/04_ground_claims.py
ground_status=$?
echo "GROUND_WITNESS_EXIT=$ground_status"

echo "SUMMARY odd_extract=$odd_extract_status even_extract=$even_extract_status solution_parse=$solution_parse_status odd_parse=$odd_parse_status even_parse=$even_parse_status odd_cmp=$odd_cmp_status even_cmp=$even_cmp_status hashes=$hash_status ground=$ground_status"

if [[ $odd_extract_status -eq 0 &&
      $even_extract_status -eq 0 &&
      $solution_parse_status -eq 0 &&
      $odd_parse_status -eq 0 &&
      $even_parse_status -eq 0 &&
      $odd_cmp_status -eq 0 &&
      $even_cmp_status -eq 0 &&
      $hash_status -eq 0 &&
      $ground_status -eq 0 ]]; then
  exit 0
fi
exit 1
