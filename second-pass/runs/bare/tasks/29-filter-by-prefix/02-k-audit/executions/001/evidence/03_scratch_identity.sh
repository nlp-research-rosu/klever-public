#!/usr/bin/env bash
set -u

overall=0
for name in solution.py solution.mpy semantic.k verification.k spec.k prove.sh
do
  printf 'COMMAND: cmp -s /candidate/%s /tmp/audit-work/candidate/%s\n' "$name" "$name"
  cmp -s "/candidate/$name" "/tmp/audit-work/candidate/$name"
  status=$?
  printf 'EXIT: %s\n' "$status"
  if test "$status" -ne 0; then
    overall=1
  fi
done

printf '%s\n' 'COMMAND: sha256sum copied proof sources'
sha256sum \
  /tmp/audit-work/candidate/solution.py \
  /tmp/audit-work/candidate/solution.mpy \
  /tmp/audit-work/candidate/semantic.k \
  /tmp/audit-work/candidate/verification.k \
  /tmp/audit-work/candidate/spec.k
status=$?
printf 'EXIT: %s\n' "$status"
if test "$status" -ne 0; then
  overall=1
fi

printf '%s\n' 'Candidate compiled definitions/caches were not copied.'
exit "$overall"
