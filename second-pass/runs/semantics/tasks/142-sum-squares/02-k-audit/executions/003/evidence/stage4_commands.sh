#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/reconstruction
cd "$scratch" || exit 90

echo "COMMAND: kast solution.mpy --definition audit-verification-kompiled --module MPY-SYNTAX --sort Module --expand-macros --output json --output-file solution-kast.json"
kast solution.mpy --definition audit-verification-kompiled --module MPY-SYNTAX --sort Module --expand-macros --output json --output-file solution-kast.json
s1=$?
echo "SOLUTION_KAST_EXIT_STATUS=$s1"

echo "COMMAND: kast --expression sumSquaresFunctionBody --definition audit-verification-kompiled --module SUM-SQUARES-VERIFICATION --sort Stmts --expand-macros --output json --output-file function-body-kast.json"
kast --expression 'sumSquaresFunctionBody' --definition audit-verification-kompiled --module SUM-SQUARES-VERIFICATION --sort Stmts --expand-macros --output json --output-file function-body-kast.json
s2=$?
echo "FUNCTION_MACRO_KAST_EXIT_STATUS=$s2"

echo "COMMAND: kast --expression sumSquaresLoopBody --definition audit-verification-kompiled --module SUM-SQUARES-VERIFICATION --sort Stmts --expand-macros --output json --output-file loop-body-kast.json"
kast --expression 'sumSquaresLoopBody' --definition audit-verification-kompiled --module SUM-SQUARES-VERIFICATION --sort Stmts --expand-macros --output json --output-file loop-body-kast.json
s3=$?
echo "LOOP_MACRO_KAST_EXIT_STATUS=$s3"

echo "COMMAND: python3 /audit-output/evidence/program_term_compare.py"
python3 /audit-output/evidence/program_term_compare.py
s4=$?
echo "PROGRAM_TERM_COMPARE_EXIT_STATUS=$s4"

echo "COMMAND: python3 /audit-output/evidence/claim_witnesses.py"
python3 /audit-output/evidence/claim_witnesses.py
s5=$?
echo "CLAIM_WITNESSES_EXIT_STATUS=$s5"

if (( s1 != 0 || s2 != 0 || s3 != 0 || s4 != 0 || s5 != 0 )); then
  exit 1
fi
exit 0
