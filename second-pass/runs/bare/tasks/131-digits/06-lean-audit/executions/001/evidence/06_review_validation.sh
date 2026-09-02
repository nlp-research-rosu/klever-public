#!/usr/bin/env bash
set -euxo pipefail

test "$(tail -n 2 /audit-output/REVIEW.md)" = \
  $'VERDICT: PASS\nLEGITIMACY: LEGIT'
test "$(rg -c '^VERDICT:' /audit-output/REVIEW.md)" = 1
test "$(rg -c '^LEGITIMACY:' /audit-output/REVIEW.md)" = 1
test ! -e /candidate
sha256sum /audit-output/REVIEW.md
find /audit-output/evidence -maxdepth 1 -type f -printf '%f\n' | sort
