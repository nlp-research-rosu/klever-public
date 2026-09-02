#!/usr/bin/env bash
set -euo pipefail

for path in \
  /tmp/audit-work/source/solution.py \
  /tmp/audit-work/source/solution.mpy \
  /tmp/audit-work/source/semantic.k \
  /tmp/audit-work/source/verification.k \
  /tmp/audit-work/source/spec.k \
  /tmp/audit-work/source/spec-vacuity.k \
  /tmp/audit-work/source/spec-body-sensitivity.k
do
  printf 'FILE: %s\n' "$path"
  nl -ba "$path"
done
