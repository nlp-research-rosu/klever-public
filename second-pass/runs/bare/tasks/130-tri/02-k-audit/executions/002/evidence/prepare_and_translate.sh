#!/usr/bin/env bash
set -euo pipefail

audit_work=/tmp/audit-work/130-tri-audit

printf 'COMMAND: mkdir -p %s\n' "$audit_work"
mkdir -p "$audit_work"

if find "$audit_work" -mindepth 1 -maxdepth 1 -print -quit | grep -q .; then
  printf 'ERROR: scratch destination is not empty: %s\n' "$audit_work" >&2
  exit 2
fi

printf 'COMMAND: copy candidate source artifacts and trusted inputs to scratch\n'
cp -p \
  /candidate/solution.py \
  /candidate/solution.mpy \
  /candidate/semantic.k \
  /candidate/verification.k \
  /candidate/spec.k \
  /candidate/prove.sh \
  "$audit_work/"
cp -p /reference/py2mpy.py "$audit_work/py2mpy.py"
cp -p /reference/prompt.py "$audit_work/prompt.py"
cp -p /reference/canonical.py "$audit_work/canonical.py"

printf 'COMMAND: python3 py2mpy.py solution.py > regenerated-solution.mpy\n'
(
  cd "$audit_work"
  python3 py2mpy.py solution.py > regenerated-solution.mpy
)
translate_status=$?
printf 'TRANSLATOR_EXIT_STATUS=%s\n' "$translate_status"

printf 'COMMAND: cmp -s regenerated-solution.mpy solution.mpy\n'
cmp -s "$audit_work/regenerated-solution.mpy" "$audit_work/solution.mpy"
cmp_status=$?
printf 'BYTE_IDENTITY_EXIT_STATUS=%s\n' "$cmp_status"

printf 'COMMAND: sha256sum solution.mpy regenerated-solution.mpy\n'
sha256sum "$audit_work/solution.mpy" "$audit_work/regenerated-solution.mpy"

printf 'SCRATCH CONTENTS\n'
find "$audit_work" -mindepth 1 -maxdepth 1 -printf '%y %f -> %l\n' | sort

