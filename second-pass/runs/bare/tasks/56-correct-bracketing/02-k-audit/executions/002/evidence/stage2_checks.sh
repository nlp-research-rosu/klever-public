#!/usr/bin/env bash
set -uo pipefail

python3 /tmp/audit-work/reference/py2mpy.py \
  /tmp/audit-work/proof/solution.py \
  > /tmp/audit-work/proof/solution.regenerated.mpy
translator_exit=$?
printf 'translator exit=%s\n' "$translator_exit"

sha256sum \
  /tmp/audit-work/proof/solution.mpy \
  /tmp/audit-work/proof/solution.regenerated.mpy

cmp -s \
  /tmp/audit-work/proof/solution.mpy \
  /tmp/audit-work/proof/solution.regenerated.mpy
cmp_exit=$?
printf 'solution.mpy byte-identity cmp exit=%s\n' "$cmp_exit"

python3 /audit-output/evidence/differential_test.py
differential_exit=$?
printf 'differential test exit=%s\n' "$differential_exit"

if (( translator_exit != 0 || cmp_exit != 0 || differential_exit != 0 )); then
  exit 1
fi
