#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/160-do-algebra
definition="$scratch/audit-verification-kompiled"
log=/audit-output/evidence/03f_kprove_all.log

if [[ ! -d "$definition" ]]; then
  echo "ERROR: fresh reviewer definition from 03_reconstruct.sh is absent"
  exit 90
fi

command=(
  kprove "$scratch/spec.k"
  --definition "$definition"
  --spec-module SPEC
)

printf 'COMMAND:'
printf ' %q' "${command[@]}"
printf '\n'
{
  printf 'COMMAND:'
  printf ' %q' "${command[@]}"
  printf '\n'
} > "$log"
"${command[@]}" 2>&1 | tee -a "$log"
status=${PIPESTATUS[0]}
printf 'EXIT_STATUS=%d\n' "$status" | tee -a "$log"
exit "$status"
