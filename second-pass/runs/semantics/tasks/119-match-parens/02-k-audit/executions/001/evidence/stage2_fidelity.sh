#!/usr/bin/env bash
set -u
source /audit-output/evidence/run_logged.sh

run_cmd mkdir -p /tmp/audit-work/audit-119-match-parens
run_cmd cp /candidate/solution.py /tmp/audit-work/audit-119-match-parens/solution.py
run_cmd cp /candidate/solution.mpy /tmp/audit-work/audit-119-match-parens/submitted-solution.mpy
run_cmd cp /candidate/spec.k /tmp/audit-work/audit-119-match-parens/spec.k
run_cmd cp /candidate/verification.k /tmp/audit-work/audit-119-match-parens/verification.k
run_cmd cp /candidate/concrete-tests.mpy /tmp/audit-work/audit-119-match-parens/concrete-tests.mpy
run_cmd cp -R /reference/reference-semantics /tmp/audit-work/audit-119-match-parens/reference-semantics
run_cmd cp /reference/py2mpy.py /tmp/audit-work/audit-119-match-parens/py2mpy.py
run_cmd cp /reference/prompt.py /tmp/audit-work/audit-119-match-parens/prompt.py
run_cmd cp /reference/canonical.py /tmp/audit-work/audit-119-match-parens/canonical.py

run_shell 'cd /tmp/audit-work/audit-119-match-parens && python3 ./py2mpy.py ./solution.py > ./regenerated-solution.mpy'
run_shell 'cd /tmp/audit-work/audit-119-match-parens && cmp -s ./regenerated-solution.mpy ./submitted-solution.mpy; rc=$?; if test "$rc" -eq 0; then echo SOLUTION_MPY_BYTE_IDENTICAL; else echo SOLUTION_MPY_MISMATCH; diff -u ./submitted-solution.mpy ./regenerated-solution.mpy; fi; exit "$rc"'
run_shell 'cd /tmp/audit-work/audit-119-match-parens && sha256sum solution.py submitted-solution.mpy regenerated-solution.mpy spec.k verification.k reference-semantics/semantics.k'
run_cmd python3 /audit-output/evidence/differential_match_parens.py
