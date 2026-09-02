#!/usr/bin/env bash
set -u
source /audit-output/evidence/run_logged.sh

run_shell 'cd /tmp/audit-work/audit-119-match-parens && kprove spec.k --definition verification-kompiled --spec-module MATCH-PARENS-SPEC --claims loopCorrect --output pretty'
run_shell 'cd /tmp/audit-work/audit-119-match-parens && kprove spec.k --definition verification-kompiled --spec-module MATCH-PARENS-SPEC --claims loopCorrect,loopFirstCorrect --trusted loopCorrect --output pretty'
run_shell 'cd /tmp/audit-work/audit-119-match-parens && kprove spec.k --definition verification-kompiled --spec-module MATCH-PARENS-SPEC --claims loopCorrect,loopFirstCorrect,isGoodCorrect --trusted loopCorrect,loopFirstCorrect --output pretty'
run_shell 'cd /tmp/audit-work/audit-119-match-parens && kprove spec.k --definition verification-kompiled --spec-module MATCH-PARENS-SPEC --claims goodBranchCorrect --output pretty'
run_shell 'cd /tmp/audit-work/audit-119-match-parens && kprove spec.k --definition verification-kompiled --spec-module MATCH-PARENS-SPEC --claims loopCorrect,loopFirstCorrect,isGoodCorrect,goodBranchCorrect,matchParensCorrect --trusted loopCorrect,loopFirstCorrect,isGoodCorrect,goodBranchCorrect --output pretty'
