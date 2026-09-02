#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/case91
evidence=/audit-output/evidence
overall=0

for source in \
  stage5-strip-fixed-spec.k \
  stage5-strip-bridge-spec.k \
  stage5-strip-opposite-spec.k \
  stage5-body-mutation.k \
  stage5-body-mutation-spec.k
do
  cp "$evidence/$source" "$scratch/$source"
  ec=$?
  if [[ $ec -ne 0 ]]; then
    printf 'COPY_FAILED %s exit=%d\n' "$source" "$ec"
    overall=1
  fi
done

run_positive() {
  local label=$1
  shift
  (
    printf 'COMMAND:'
    printf ' %q' "$@"
    printf '\nWORKDIR: %s\n' "$scratch"
    cd "$scratch"
    "$@"
    ec=$?
    printf 'EXIT_STATUS=%d\n' "$ec"
    exit "$ec"
  ) > "$evidence/$label.log" 2>&1
  ec=$?
  printf '%s=%d\n' "$label" "$ec"
  if [[ $ec -ne 0 ]]; then overall=1; fi
}

run_negative() {
  local label=$1
  shift
  (
    printf 'COMMAND:'
    printf ' %q' "$@"
    printf '\nWORKDIR: %s\n' "$scratch"
    cd "$scratch"
    "$@"
    ec=$?
    printf 'EXIT_STATUS=%d\n' "$ec"
    exit "$ec"
  ) > "$evidence/$label.log" 2>&1
  ec=$?
  printf '%s=%d (expected nonzero)\n' "$label" "$ec"
  if [[ $ec -eq 0 ]]; then
    overall=1
  elif ! rg -q 'WarnStuckClaimState' "$evidence/$label.log"; then
    printf '%s missing expected WarnStuckClaimState\n' "$label"
    overall=1
  fi
}

run_positive stage5_kprove_strip_fixed \
  kprove stage5-strip-fixed-spec.k \
  --definition audit-connection-kompiled \
  --spec-module STAGE5-STRIP-FIXED-SPEC

run_positive stage5_kprove_strip_bridge \
  kprove stage5-strip-bridge-spec.k \
  --definition audit-verification-base-kompiled \
  --spec-module STAGE5-STRIP-BRIDGE-SPEC

run_negative stage5_kprove_strip_opposite \
  kprove stage5-strip-opposite-spec.k \
  --definition audit-verification-base-kompiled \
  --spec-module STAGE5-STRIP-OPPOSITE-SPEC

run_positive stage5_kompile_body_mutation \
  kompile --backend haskell stage5-body-mutation.k \
  --main-module STAGE5-BODY-MUTATION \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-stage5-body-mutation-kompiled

run_negative stage5_kprove_body_mutation \
  kprove stage5-body-mutation-spec.k \
  --definition audit-stage5-body-mutation-kompiled \
  --spec-module STAGE5-BODY-MUTATION-SPEC

printf 'FINAL_STATUS=%d\n' "$overall"
exit "$overall"
