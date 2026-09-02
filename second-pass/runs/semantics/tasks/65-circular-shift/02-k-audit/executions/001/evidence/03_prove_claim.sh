#!/usr/bin/env bash
set -u
if test "$#" -ne 1; then
  printf 'usage: %s CLAIM-LABEL\n' "$0" >&2
  exit 64
fi
claim=$1
cd /tmp/audit-work/case || exit 125

printf '$ kprove --definition verification-kompiled --spec-module CIRCULAR-SHIFT-SPEC --claims %s --depth 300 --warnings none spec.k\n' "$claim"
kprove \
  --definition verification-kompiled \
  --spec-module CIRCULAR-SHIFT-SPEC \
  --claims "$claim" \
  --depth 300 \
  --warnings none \
  spec.k
rc=$?
printf '[exit %d]\n' "$rc"
exit "$rc"
