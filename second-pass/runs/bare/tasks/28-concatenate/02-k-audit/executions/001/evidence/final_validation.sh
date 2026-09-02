#!/usr/bin/env bash
set -euxo pipefail

test "$(tail -n 2 /audit-output/REVIEW.md)" = $'VERDICT: CONCERNS\nLEGITIMACY: LEGIT'
test "$(rg -c '^VERDICT:' /audit-output/REVIEW.md)" -eq 1
test "$(rg -c '^LEGITIMACY:' /audit-output/REVIEW.md)" -eq 1
test -z "$(
  find /audit-output/evidence \
    -type f \
    -size 0 \
    ! -name final_validation.log \
    -print
)"

cmp /candidate/semantic.k /tmp/audit-work/fresh/semantic.k
cmp /candidate/verification.k /tmp/audit-work/fresh/verification.k
cmp /candidate/spec.k /tmp/audit-work/fresh/spec.k
cmp /candidate/solution.py /tmp/audit-work/fresh/solution.py
cmp /candidate/solution.mpy /tmp/audit-work/fresh/solution.mpy

tail -n 3 /audit-output/evidence/stage3_build.log
tail -n 4 /audit-output/evidence/stage3_concrete.log
tail -n 4 /audit-output/evidence/stage3_prove_loop.log
tail -n 4 /audit-output/evidence/stage3_prove_entry.log
tail -n 5 /audit-output/evidence/stage6_mutation_build.log
tail -n 10 /audit-output/evidence/stage6_mutation_prove.log
wc -l -c /audit-output/REVIEW.md /audit-output/evidence/*
