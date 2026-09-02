#!/usr/bin/env bash
set -uo pipefail

cd /tmp/audit-work/review-57/src || exit 1

printf 'COMMAND: rg -n local declaration/rule/claim/configuration lines\n'
rg -n '^[[:space:]]*(requires|module|endmodule|imports|configuration|syntax|rule|claim)([[:space:]]|$)' \
  semantic.k verification.k spec.k
status=$?
printf 'EXIT_STATUS: %d\n\n' "$status"
(( status == 0 )) || exit "$status"

printf 'COMMAND: rg -n proof-relevant attributes\n'
rg -n '\[(function|total|functional|simplification|concrete|macro|owise|priority|anywhere)' \
  semantic.k verification.k spec.k
status=$?
printf 'EXIT_STATUS: %d\n\n' "$status"
(( status == 0 )) || exit "$status"

printf 'COMMAND: rg -n opaque/fresh/priority/simplification/total markers (exit 1 means absent)\n'
rg -n '(opaque|fresh|priority|simplification|\\[total\\]|\\[functional\\]|\\[concrete\\]|\\[macro\\]|\\[owise\\])' \
  semantic.k verification.k spec.k
status=$?
printf 'EXIT_STATUS: %d (expected 1: no matches)\n\n' "$status"
(( status == 1 )) || exit 1

printf 'COMMAND: nl -ba semantic.k verification.k spec.k\n'
for file in semantic.k verification.k spec.k; do
  printf '===== %s =====\n' "$file"
  nl -ba "$file"
done
status=$?
printf 'EXIT_STATUS: %d\n' "$status"
exit "$status"
