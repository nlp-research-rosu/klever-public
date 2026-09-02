#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/candidate-fresh
definition="$scratch/verification-haskell-kompiled"
extracted="$scratch/extracted-claim-program.mpy"
solution_kore="$scratch/solution-program.kore"
claim_kore="$scratch/claim-program.kore"

echo 'COMMAND: python3 /audit-output/evidence/stage4/pinning_check.py'
python3 /audit-output/evidence/stage4/pinning_check.py
text_status=$?
echo "TEXTUAL_PINNING_EXIT_STATUS=$text_status"
if [[ "$text_status" -ne 0 ]]; then
  exit "$text_status"
fi

echo 'COMMAND: python3 pinning_check.py --emit-extracted > extracted-claim-program.mpy'
python3 /audit-output/evidence/stage4/pinning_check.py --emit-extracted \
  > "$extracted"
extract_status=$?
echo "EXTRACTION_EXIT_STATUS=$extract_status"
if [[ "$extract_status" -ne 0 ]]; then
  exit "$extract_status"
fi

echo 'COMMAND: kast solution.mpy --definition verification-haskell-kompiled --module MPY-SYNTAX --sort Pgm --output kore --output-file solution-program.kore'
(
  cd "$scratch" &&
  kast \
    solution.mpy \
    --definition "$definition" \
    --module MPY-SYNTAX \
    --sort Pgm \
    --output kore \
    --output-file "$solution_kore"
)
solution_status=$?
echo "SOLUTION_KAST_EXIT_STATUS=$solution_status"
if [[ "$solution_status" -ne 0 ]]; then
  exit "$solution_status"
fi

echo 'COMMAND: kast extracted-claim-program.mpy --definition verification-haskell-kompiled --module MPY-SYNTAX --sort Pgm --output kore --output-file claim-program.kore'
(
  cd "$scratch" &&
  kast \
    "$extracted" \
    --definition "$definition" \
    --module MPY-SYNTAX \
    --sort Pgm \
    --output kore \
    --output-file "$claim_kore"
)
claim_status=$?
echo "CLAIM_KAST_EXIT_STATUS=$claim_status"
if [[ "$claim_status" -ne 0 ]]; then
  exit "$claim_status"
fi

echo 'COMMAND: cmp -s solution-program.kore claim-program.kore'
cmp -s "$solution_kore" "$claim_kore"
kore_cmp_status=$?
echo "KORE_IDENTITY_EXIT_STATUS=$kore_cmp_status"
sha256sum "$solution_kore" "$claim_kore"
if [[ "$kore_cmp_status" -ne 0 ]]; then
  diff -u "$solution_kore" "$claim_kore" || true
fi
exit "$kore_cmp_status"
