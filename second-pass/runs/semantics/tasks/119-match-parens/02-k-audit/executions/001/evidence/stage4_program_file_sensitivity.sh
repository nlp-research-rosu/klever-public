#!/usr/bin/env bash
set -u
source /audit-output/evidence/run_logged.sh

run_shell 'cd /tmp/audit-work/audit-119-match-parens && mv solution.mpy solution.mpy.held && trap '"'"'mv solution.mpy.held solution.mpy'"'"' EXIT && test ! -e solution.mpy && kprove spec.k --definition verification-kompiled --spec-module MATCH-PARENS-SPEC --claims loopCorrect,loopFirstCorrect,isGoodCorrect,goodBranchCorrect,matchParensCorrect --trusted loopCorrect,loopFirstCorrect,isGoodCorrect,goodBranchCorrect --output pretty'
run_shell 'cd /tmp/audit-work/audit-119-match-parens && test -f solution.mpy && cmp -s solution.mpy submitted-solution.mpy'
