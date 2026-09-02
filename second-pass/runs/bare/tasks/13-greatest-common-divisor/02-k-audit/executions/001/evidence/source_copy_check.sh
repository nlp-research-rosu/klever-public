#!/usr/bin/env bash
set -u

status=0
for name in \
  semantic.k solution.py solution.mpy spec.k verification.k gcd-spec.k \
  loop-spec.k loop-verification.k prove.sh
do
  if cmp -s "/candidate/$name" "/tmp/audit-work/source/$name"; then
    printf 'IDENTICAL candidate->scratch %s\n' "$name"
  else
    printf 'MISMATCH candidate->scratch %s\n' "$name"
    status=1
  fi
done
printf '%s\n' 'SCRATCH_SOURCE_SHA256'
sha256sum \
  /tmp/audit-work/source/semantic.k \
  /tmp/audit-work/source/solution.py \
  /tmp/audit-work/source/solution.mpy \
  /tmp/audit-work/source/spec.k \
  /tmp/audit-work/source/verification.k \
  /tmp/audit-work/source/gcd-spec.k \
  /tmp/audit-work/source/loop-spec.k \
  /tmp/audit-work/source/loop-verification.k
exit "$status"
