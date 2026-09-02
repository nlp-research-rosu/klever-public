#!/usr/bin/env bash
set -u
source /audit-output/evidence/run_logged.sh

run_cmd cp /audit-output/evidence/spec-vacuity-ground.k /tmp/audit-work/audit-119-match-parens/spec-vacuity-ground.k
run_shell 'cd /tmp/audit-work/audit-119-match-parens && kprove spec-vacuity-ground.k --definition verification-kompiled --spec-module MATCH-PARENS-SPEC-VACUITY-GROUND --claims matchParensGroundFalseResult --dry-run > vacuity-ground-dry-run.kore; rc=$?; wc -c vacuity-ground-dry-run.kore; sha256sum vacuity-ground-dry-run.kore; exit "$rc"'
run_shell 'cd /tmp/audit-work/audit-119-match-parens && kprove spec-vacuity-ground.k --definition verification-kompiled --spec-module MATCH-PARENS-SPEC-VACUITY-GROUND --claims matchParensGroundFalseResult --output pretty'
