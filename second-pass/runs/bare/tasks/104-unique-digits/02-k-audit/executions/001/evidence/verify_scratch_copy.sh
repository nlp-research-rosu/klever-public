#!/usr/bin/env bash
set -u

status=0
for name in semantic.k solution.py solution.mpy spec.k verification.k prove.sh; do
  if cmp -s "/candidate/$name" \
      "/tmp/audit-work/104-unique-digits/candidate/$name"; then
    printf 'IDENTICAL %s\n' "$name"
  else
    printf 'DIFFERENT %s\n' "$name"
    status=1
  fi
done

printf '%s\n' 'SCRATCH SOURCE HASHES'
sha256sum \
  /tmp/audit-work/104-unique-digits/candidate/semantic.k \
  /tmp/audit-work/104-unique-digits/candidate/solution.py \
  /tmp/audit-work/104-unique-digits/candidate/solution.mpy \
  /tmp/audit-work/104-unique-digits/candidate/spec.k \
  /tmp/audit-work/104-unique-digits/candidate/verification.k \
  /tmp/audit-work/104-unique-digits/candidate/prove.sh

exit "$status"
