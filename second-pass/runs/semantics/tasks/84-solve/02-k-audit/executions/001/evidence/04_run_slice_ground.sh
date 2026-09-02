#!/usr/bin/env bash
set -u

printf '$ kprove /audit-output/evidence/04_slice_ground.k --definition /tmp/audit-work/base-semantics-kompiled --spec-module SLICE-GROUND --output pretty\n'
kprove /audit-output/evidence/04_slice_ground.k \
  --definition /tmp/audit-work/base-semantics-kompiled \
  --spec-module SLICE-GROUND \
  --output pretty
rc=$?
printf '[exit %d]\n' "$rc"
exit "$rc"
