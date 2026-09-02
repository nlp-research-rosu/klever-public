#!/usr/bin/env bash
set -euo pipefail
set -x

test "$(rg -c '^VERDICT:' /audit-output/REVIEW.md)" -eq 1
test "$(rg -c '^LEGITIMACY:' /audit-output/REVIEW.md)" -eq 1
test "$(tail -n 2 /audit-output/REVIEW.md | sed -n '1p')" = \
  "VERDICT: PASS"
test "$(tail -n 1 /audit-output/REVIEW.md)" = \
  "LEGITIMACY: LEGIT"
sha256sum /audit-output/REVIEW.md
tail -n 8 /audit-output/REVIEW.md
find /audit-output/evidence -maxdepth 1 -type f -print | sort
