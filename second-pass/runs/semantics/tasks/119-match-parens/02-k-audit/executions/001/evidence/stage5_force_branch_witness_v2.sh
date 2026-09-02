#!/usr/bin/env bash
set -u
source /audit-output/evidence/run_logged.sh

run_cmd cp /audit-output/evidence/force-branch-witness.k /tmp/audit-work/audit-119-match-parens/force-branch-witness.k
run_shell 'cd /tmp/audit-work/audit-119-match-parens && kompile force-branch-witness.k --backend haskell --main-module FORCE-BRANCH-WITNESS --syntax-module MPY-SYNTAX --output-definition force-branch-witness-v2-kompiled'
run_shell 'cd /tmp/audit-work/audit-119-match-parens && kprove force-branch-witness-spec.k --definition force-branch-witness-v2-kompiled --spec-module FORCE-BRANCH-WITNESS-SPEC --claims bridgeChoosesThen --output pretty'
run_shell 'cd /tmp/audit-work/audit-119-match-parens && kprove force-branch-witness-spec.k --definition force-branch-witness-v2-kompiled --spec-module FORCE-BRANCH-WITNESS-SPEC --claims nativeChoosesElse --output pretty'
