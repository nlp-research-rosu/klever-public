#!/usr/bin/env bash
set -u
source /audit-output/evidence/run_logged.sh

run_cmd python3 /audit-output/evidence/concrete_claim_witnesses.py
run_shell 'cd /tmp/audit-work/audit-119-match-parens && rg -n "solution\\.mpy|submitted-solution|Module\\(|matchParensClosure|matchParensBody|isGoodClosure|isGoodBody" spec.k verification.k'
run_shell 'cd /tmp/audit-work/audit-119-match-parens && cmp -s solution.mpy submitted-solution.mpy; rc=$?; echo "scratch_solution_vs_submitted_cmp=$rc"; exit "$rc"'
