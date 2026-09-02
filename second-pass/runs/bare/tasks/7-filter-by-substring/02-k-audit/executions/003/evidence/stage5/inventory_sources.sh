#!/usr/bin/env bash
set -u

for path in /candidate/semantic.k /candidate/verification.k /candidate/spec.k; do
  printf '$ nl -ba %q\n' "$path"
  nl -ba "$path"
  printf 'EXIT: %d\n' "$?"
done

printf '%s\n' '$ rg -n "configuration|syntax |\\[function|\\[total|\\[functional|rule |claim |priority|simplification|opaque|owise|anywhere|fresh" /candidate/*.k'
rg -n \
  'configuration|syntax |\[function|\[total|\[functional|rule |claim |priority|simplification|opaque|owise|anywhere|fresh' \
  /candidate/*.k
printf 'EXIT: %d\n' "$?"
