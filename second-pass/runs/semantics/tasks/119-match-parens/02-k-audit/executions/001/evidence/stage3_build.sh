#!/usr/bin/env bash
set -u
source /audit-output/evidence/run_logged.sh

run_cmd cp /tmp/audit-work/audit-119-match-parens/submitted-solution.mpy /tmp/audit-work/audit-119-match-parens/solution.mpy
run_shell 'cd /tmp/audit-work/audit-119-match-parens && find . -maxdepth 1 \( -name "*-kompiled" -o -name ".kprove-*" \) -print'
run_shell 'cd /tmp/audit-work/audit-119-match-parens && kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition runtime-kompiled'
run_shell 'cd /tmp/audit-work/audit-119-match-parens && krun concrete-tests.mpy --definition runtime-kompiled --output none'
run_shell 'cd /tmp/audit-work/audit-119-match-parens && krun solution.mpy --definition runtime-kompiled --output pretty'
run_shell 'cd /tmp/audit-work/audit-119-match-parens && kompile verification.k --backend haskell --main-module MATCH-PARENS-VERIFICATION --syntax-module MPY-SYNTAX --output-definition verification-kompiled'
