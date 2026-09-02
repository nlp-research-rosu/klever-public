#!/usr/bin/env bash
set -u

scratch="/tmp/audit-work/37-sort-even"
log="/audit-output/evidence/02-prepare-scratch.log"

printf '%s\n' \
  'COMMAND: mkdir -p /tmp/audit-work/37-sort-even/reference-semantics' \
  'COMMAND: cp -a [explicit candidate source artifacts] /tmp/audit-work/37-sort-even/' \
  'COMMAND: cp -a /reference/{canonical.py,prompt.py,py2mpy.py} /tmp/audit-work/37-sort-even/' \
  'COMMAND: cp -a /reference/reference-semantics/. /tmp/audit-work/37-sort-even/reference-semantics/' \
  > "$log"

mkdir -p "$scratch/reference-semantics" >> "$log" 2>&1
status=$?
if [ "$status" -eq 0 ]; then
  cp -a \
    /candidate/solution.py \
    /candidate/solution.mpy \
    /candidate/verification.k \
    /candidate/spec.k \
    /candidate/prove.sh \
    /candidate/concrete-tests.py \
    /candidate/concrete-tests.mpy \
    "$scratch/" >> "$log" 2>&1
  status=$?
fi
if [ "$status" -eq 0 ]; then
  cp -a \
    /reference/canonical.py \
    /reference/prompt.py \
    /reference/py2mpy.py \
    "$scratch/" >> "$log" 2>&1
  status=$?
fi
if [ "$status" -eq 0 ]; then
  cp -a /reference/reference-semantics/. "$scratch/reference-semantics/" >> "$log" 2>&1
  status=$?
fi
find "$scratch" -maxdepth 3 -printf '%y %p -> %l\n' | sort >> "$log" 2>&1
printf 'EXIT_STATUS: %s\n' "$status" >> "$log"
exit "$status"
