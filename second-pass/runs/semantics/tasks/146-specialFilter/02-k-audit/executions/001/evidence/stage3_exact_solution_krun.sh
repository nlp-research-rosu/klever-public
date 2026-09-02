#!/usr/bin/env bash
set -u
set -o pipefail
set -x

PATH="/home/agent/.nix-profile/bin:$PATH"
work=/tmp/audit-work/candidate-clean
evidence=/audit-output/evidence

krun "$work/solution.mpy" \
  --definition "$work/runtime-kompiled" \
  --output pretty \
  2>&1 | tee "$evidence/stage3_exact_solution_krun.log"
status=${PIPESTATUS[0]}
printf 'EXACT_SOLUTION_KRUN_EXIT=%s\n' "$status"
exit "$status"
