#!/usr/bin/env bash
set -euo pipefail
trap 'status=$?; printf "[audit] exit_status=%s\n" "$status"' EXIT
set -x

review=/audit-output/REVIEW.md

test "$(tail -n 2 "$review" | head -n 1)" = "VERDICT: CONCERNS"
test "$(tail -n 1 "$review")" = "LEGITIMACY: LEGIT"
test "$(grep -c '^VERDICT:' "$review")" -eq 1
test "$(grep -c '^LEGITIMACY:' "$review")" -eq 1

for stage in 1 2 3 4 5 6 7; do
  grep -q "^## $stage\\." "$review"
done

find /audit-output/evidence -maxdepth 3 -type f -printf '%s %p\n' | sort
sha256sum "$review" /audit-output/evidence/*.sh /audit-output/evidence/*.py
wc -l -c "$review"
tail -n 8 "$review"
