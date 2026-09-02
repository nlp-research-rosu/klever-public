#!/usr/bin/env bash
set -u

printf '$ sha256sum candidate and scratch source pairs\n'
sha256sum \
  /candidate/solution.py \
  /tmp/audit-work/fresh/solution.py \
  /candidate/solution.mpy \
  /tmp/audit-work/fresh/solution.mpy \
  /candidate/semantic.k \
  /tmp/audit-work/fresh/semantic.k \
  /candidate/verification.k \
  /tmp/audit-work/fresh/verification.k \
  /candidate/spec.k \
  /tmp/audit-work/fresh/spec.k
printf '[exit %d]\n' "$?"

for name in solution.py solution.mpy semantic.k verification.k spec.k; do
  printf '\n$ cmp -s /candidate/%s /tmp/audit-work/fresh/%s\n' "$name" "$name"
  cmp -s "/candidate/$name" "/tmp/audit-work/fresh/$name"
  printf '[exit %d]\n' "$?"
done
