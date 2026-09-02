#!/usr/bin/env bash
set -euo pipefail
set -x

kompile --version
kprove --version
test ! -e /reference/reference-semantics
test ! -L /reference/reference-semantics

test "$(rg -c '^VERDICT:' /audit-output/REVIEW.md)" = 1
test "$(rg -c '^LEGITIMACY:' /audit-output/REVIEW.md)" = 1
test "$(tail -n 2 /audit-output/REVIEW.md)" = $'VERDICT: FAIL\nLEGITIMACY: NOT_LEGIT'
tail -n 2 /audit-output/REVIEW.md

find -P /audit-output/evidence -maxdepth 1 -type f \
  ! -name final_checks.log -print0 \
  | sort -z \
  | xargs -0 sha256sum

printf 'SCRIPT_EXIT=0\n'
