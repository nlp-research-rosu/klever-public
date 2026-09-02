#!/usr/bin/env bash
set -uo pipefail

cd /tmp/audit-work/reconstruction-62 || exit 70

command=(
  timeout 120s
  kprove spec.k
  --definition verification-fresh-kompiled
  --spec-module SPEC
  --claims helper-correct,derivative-nonempty
)
printf 'COMMAND:'
printf ' %q' "${command[@]}"
printf '\n'
"${command[@]}"
status=$?
printf 'EXIT_STATUS: %d\n' "$status"
exit "$status"
