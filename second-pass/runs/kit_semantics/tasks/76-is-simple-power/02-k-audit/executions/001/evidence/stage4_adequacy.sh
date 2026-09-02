#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/76-is-simple-power
status=0

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  rc=$?
  printf '[exit %d]\n' "$rc"
  if [ "$rc" -ne 0 ]; then
    status=1
  fi
}

run kast "$scratch/solution.mpy" \
  --definition "$scratch/runtime-audit-kompiled" \
  --module MPY-SYNTAX \
  --output json \
  --expand-macros \
  --output-file /audit-output/evidence/stage4-solution-kast.json

run kprove "$scratch/spec.k" \
  --definition "$scratch/verification-audit-kompiled" \
  --spec-module SPEC \
  --dry-run \
  --emit-json-spec /audit-output/evidence/stage4-spec-kast.json \
  --output none

run python3 /audit-output/evidence/program_pinning_check.py

run kprove /audit-output/evidence/spec-ground-eval.k \
  -I "$scratch" \
  --definition "$scratch/verification-audit-kompiled" \
  --spec-module SPEC-GROUND-EVAL

printf '\nSTAGE4_STATUS=%d\n' "$status"
exit "$status"
