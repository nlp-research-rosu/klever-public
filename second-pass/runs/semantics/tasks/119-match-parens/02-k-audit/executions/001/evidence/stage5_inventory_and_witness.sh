#!/usr/bin/env bash
set -u
source /audit-output/evidence/run_logged.sh

run_shell 'for f in /reference/reference-semantics/semantics.k /reference/reference-semantics/semantics/*.k /candidate/verification.k /candidate/spec.k; do echo "===== $f ====="; rg -n "^[[:space:]]*(syntax|configuration|context|rule|claim)\\b|\\[(function|total|functional|concrete|simplification|owise|priority|symbol)" "$f"; done'
run_shell 'for f in /reference/reference-semantics/semantics.k /reference/reference-semantics/semantics/*.k /candidate/verification.k /candidate/spec.k; do declarations=$(rg -c "^[[:space:]]*(syntax|configuration|context|rule|claim)\\b" "$f" || true); functions=$(rg -c "\\[(function|total|functional|concrete|simplification|owise|priority|symbol)" "$f" || true); printf "%s declarations=%s attributed_lines=%s\\n" "$f" "$declarations" "$functions"; done'
run_shell 'rg -n "opaque|oracle|trusted|\\[total\\]|\\[functional\\]|\\[concrete\\]|\\[simplification\\]|priority\\(" /reference/reference-semantics /candidate/verification.k /candidate/spec.k'

run_cmd cp /audit-output/evidence/force-branch-witness.k /tmp/audit-work/audit-119-match-parens/force-branch-witness.k
run_cmd cp /audit-output/evidence/force-branch-witness-spec.k /tmp/audit-work/audit-119-match-parens/force-branch-witness-spec.k
run_shell 'cd /tmp/audit-work/audit-119-match-parens && kompile force-branch-witness.k --backend haskell --main-module FORCE-BRANCH-WITNESS --syntax-module MPY-SYNTAX --output-definition force-branch-witness-kompiled'
run_shell 'cd /tmp/audit-work/audit-119-match-parens && kprove force-branch-witness-spec.k --definition force-branch-witness-kompiled --spec-module FORCE-BRANCH-WITNESS-SPEC --claims bridgeChoosesThen --output pretty'
run_shell 'cd /tmp/audit-work/audit-119-match-parens && kprove force-branch-witness-spec.k --definition force-branch-witness-kompiled --spec-module FORCE-BRANCH-WITNESS-SPEC --claims nativeChoosesElse --output pretty'
