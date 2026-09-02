#!/usr/bin/env bash
set -u
source /audit-output/evidence/run_logged.sh

run_cmd cp /audit-output/evidence/spec-vacuity.k /tmp/audit-work/audit-119-match-parens/spec-vacuity.k
run_shell 'diff -u /candidate/spec.k /audit-output/evidence/spec-vacuity.k'
run_shell 'cd /tmp/audit-work/audit-119-match-parens && kprove spec-vacuity.k --definition verification-kompiled --spec-module MATCH-PARENS-SPEC-VACUITY --claims loopCorrect,loopFirstCorrect,isGoodCorrect,goodBranchCorrect,matchParensFalseResult --trusted loopCorrect,loopFirstCorrect,isGoodCorrect,goodBranchCorrect --dry-run > vacuity-dry-run.kore; rc=$?; wc -c vacuity-dry-run.kore; sha256sum vacuity-dry-run.kore; exit "$rc"'
run_shell 'cd /tmp/audit-work/audit-119-match-parens && kprove spec-vacuity.k --definition verification-kompiled --spec-module MATCH-PARENS-SPEC-VACUITY --claims loopCorrect,loopFirstCorrect,isGoodCorrect,goodBranchCorrect,matchParensFalseResult --trusted loopCorrect,loopFirstCorrect,isGoodCorrect,goodBranchCorrect --output pretty'
