#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/130-tri-audit
evidence=/audit-output/evidence
overall=0

run_expect_zero() {
  name=$1
  shift
  log="$evidence/$name.full.log"
  printf '\nCOMMAND:'
  printf ' %q' "$@"
  printf '\nFULL_LOG: %s\n' "$log"
  "$@" >"$log" 2>&1
  status=$?
  printf 'EXIT_STATUS: %d EXPECTED: 0\n' "$status"
  sed -n '1,180p' "$log"
  if [[ "$status" -ne 0 ]]; then overall=1; fi
}

run_expect_nonzero_stuck() {
  name=$1
  shift
  log="$evidence/$name.full.log"
  printf '\nCOMMAND:'
  printf ' %q' "$@"
  printf '\nFULL_LOG: %s\n' "$log"
  "$@" >"$log" 2>&1
  status=$?
  printf 'EXIT_STATUS: %d EXPECTED: nonzero\n' "$status"
  if [[ $(wc -l < "$log") -le 220 ]]; then
    sed -n '1,220p' "$log"
  else
    sed -n '1,110p' "$log"
    printf '%s\n' '... OUTPUT BOUNDED; FULL LOG PRESERVED ...'
    tail -n 110 "$log"
  fi
  if [[ "$status" -eq 0 ]]; then overall=1; fi
  if ! grep -q 'WarnStuckClaimState' "$log"; then
    printf 'EXPECTED_STUCK_RESIDUAL_MISSING\n'
    overall=1
  fi
}

run_expect_zero stage5_bridge_enabled_false_state \
  kprove "$evidence/bridge_witness_spec.k" \
  --definition "$scratch/verification-audit-kompiled" \
  --spec-module BRIDGE-WITNESS-SPEC \
  --output pretty

run_expect_zero stage5_neutral_build \
  kompile "$evidence/neutral_verification.k" \
  --backend haskell \
  --main-module TRI-NEUTRAL-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition "$scratch/neutral-audit-kompiled"

run_expect_nonzero_stuck stage5_bridge_free_rejects_false_state \
  kprove "$evidence/neutral_witness_spec.k" \
  --definition "$scratch/neutral-audit-kompiled" \
  --spec-module NEUTRAL-WITNESS-SPEC \
  --output pretty

top_count=$(grep -c '^#Top$' "$evidence/stage5_bridge_enabled_false_state.full.log" || true)
printf 'BRIDGE_ENABLED_TOP_COUNT: %s\n' "$top_count"
if [[ "$top_count" -ne 1 ]]; then overall=1; fi

printf '\nSTAGE5_BRIDGE_WITNESS_EXIT_STATUS: %d\n' "$overall"
exit "$overall"
