#!/usr/bin/env bash
set -u
source /audit-output/evidence/run_logged.sh

run_cmd wc -l -c /audit-output/REVIEW.md
run_shell 'rg -n "^## [1-7]\\." /audit-output/REVIEW.md'
run_shell 'tail -n 2 /audit-output/REVIEW.md'
run_shell 'test "$(rg -c "^VERDICT: (PASS|CONCERNS|FAIL)$" /audit-output/REVIEW.md)" -eq 1 && test "$(rg -c "^LEGITIMACY: (LEGIT|NOT_LEGIT)$" /audit-output/REVIEW.md)" -eq 1'
