#!/usr/bin/env bash
set -u

log="/audit-output/evidence/final-checks.log"
scratch="/tmp/audit-work/reconstruction"
exec >"$log" 2>&1

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return 0
}

for source in solution.py solution.mpy semantic.k verification.k spec.k; do
  run cmp -s "/candidate/$source" "$scratch/$source"
done
run tail -n 2 /audit-output/REVIEW.md
run bash -c 'test "$(tail -n 2 /audit-output/REVIEW.md)" = $'"'"'VERDICT: CONCERNS\nLEGITIMACY: LEGIT'"'"
run bash -c 'test "$(rg -c "^VERDICT:|^LEGITIMACY:" /audit-output/REVIEW.md)" = 2'
run find /audit-output/evidence -maxdepth 1 -type f -printf '%f %s bytes\n'
run sha256sum /audit-output/REVIEW.md
