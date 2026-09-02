#!/usr/bin/env bash
set -euo pipefail

printf '%s\n' 'COMMAND: find /candidate -maxdepth 1 -type f -name *.k -printf %f\\n | sort'
find /candidate -maxdepth 1 -type f -name '*.k' -printf '%f\n' | sort
printf 'EXIT_STATUS: %d\n' "$?"

for file in /candidate/semantic.k /candidate/verification.k /candidate/spec.k; do
  printf 'COMMAND: nl -ba %q\n' "$file"
  nl -ba "$file"
  printf 'EXIT_STATUS: %d\n' "$?"
done

printf '%s\n' \
  "COMMAND: rg -n '^\\s*(module|imports|syntax|configuration|rule|claim)|\\[(function|total|functional|macro|simplification|priority|owise|concrete|trusted)' /candidate/semantic.k /candidate/verification.k /candidate/spec.k"
rg -n \
  '^\s*(module|imports|syntax|configuration|rule|claim)|\[(function|total|functional|macro|simplification|priority|owise|concrete|trusted)' \
  /candidate/semantic.k /candidate/verification.k /candidate/spec.k
printf 'EXIT_STATUS: %d\n' "$?"
