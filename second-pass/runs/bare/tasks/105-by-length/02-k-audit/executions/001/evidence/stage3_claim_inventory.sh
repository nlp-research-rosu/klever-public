#!/usr/bin/env bash
set +e
set -x

rg -n '^[[:space:]]*claim([[:space:]]|$)' \
  /tmp/audit-work/source/semantic.k \
  /tmp/audit-work/source/verification.k \
  /tmp/audit-work/source/spec.k
claim_search_exit=$?
printf 'positive claim inventory exit: %s\n' "$claim_search_exit"
exit "$claim_search_exit"
