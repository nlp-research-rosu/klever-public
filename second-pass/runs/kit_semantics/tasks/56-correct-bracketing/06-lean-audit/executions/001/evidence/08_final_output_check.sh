#!/usr/bin/env bash
set -o errexit -o nounset -o pipefail

printf 'COMMAND: verify REVIEW.md has one verdict and one legitimacy line and ends with the required pair\n'
test "$(rg -c '^VERDICT:' /audit-output/REVIEW.md)" -eq 1
test "$(rg -c '^LEGITIMACY:' /audit-output/REVIEW.md)" -eq 1
test "$(tail -n 2 /audit-output/REVIEW.md | sed -n '1p')" = 'VERDICT: PASS'
test "$(tail -n 2 /audit-output/REVIEW.md | sed -n '2p')" = 'LEGITIMACY: LEGIT'
tail -n 2 /audit-output/REVIEW.md

printf '\nCOMMAND: list audit evidence artifacts\n'
rg --files /audit-output/evidence | sort
