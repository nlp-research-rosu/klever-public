#!/usr/bin/env bash
set -u

review=/audit-output/REVIEW.md
expected=$'VERDICT: CONCERNS\nLEGITIMACY: LEGIT'

printf '+ tail -n 2 %q\n' "$review"
tail -n 2 "$review"
tail_status=$?
printf 'EXIT_STATUS=%d\n' "$tail_status"

actual=$(tail -n 2 "$review")
printf '+ test "$actual" = "$expected"\n'
test "$actual" = "$expected"
marker_status=$?
printf 'EXIT_STATUS=%d\n' "$marker_status"

printf '+ test "$(rg -c "^VERDICT:" "$review")" = 1\n'
test "$(rg -c '^VERDICT:' "$review")" = 1
verdict_count_status=$?
printf 'EXIT_STATUS=%d\n' "$verdict_count_status"

printf '+ test "$(rg -c "^LEGITIMACY:" "$review")" = 1\n'
test "$(rg -c '^LEGITIMACY:' "$review")" = 1
legitimacy_count_status=$?
printf 'EXIT_STATUS=%d\n' "$legitimacy_count_status"

printf '+ test -z "$(rg "/candidate/verification-kompiled" /audit-output/evidence/03-rebuild-clean.log || true)"\n'
candidate_cache_reference=$(rg '/candidate/verification-kompiled' \
  /audit-output/evidence/03-rebuild-clean.log || true)
test -z "$candidate_cache_reference"
cache_status=$?
printf 'EXIT_STATUS=%d\n' "$cache_status"

printf '+ find /audit-output/evidence -maxdepth 1 -type f -printf "%%f %%s bytes\\n" | sort\n'
find /audit-output/evidence -maxdepth 1 -type f -printf '%f %s bytes\n' | sort
find_status=$?
printf 'EXIT_STATUS=%d\n' "$find_status"

printf '+ sha256sum %q\n' "$review"
sha256sum "$review"
hash_status=$?
printf 'EXIT_STATUS=%d\n' "$hash_status"

if (( tail_status != 0 || marker_status != 0 ||
      verdict_count_status != 0 || legitimacy_count_status != 0 ||
      cache_status != 0 || find_status != 0 || hash_status != 0 )); then
  exit 1
fi
exit 0
