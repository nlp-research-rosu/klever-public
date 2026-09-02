#!/usr/bin/env bash
set -uo pipefail

work=/tmp/audit-work/reconstruction
evidence=/audit-output/evidence
cd "$work" || exit 1

run_logged() {
  local label=$1
  shift
  local log="$evidence/$label.log"
  {
    printf 'COMMAND:'
    printf ' %q' "$@"
    printf '\n'
  } | tee "$log"
  "$@" 2>&1 | tee -a "$log"
  local status=${PIPESTATUS[0]}
  printf 'EXIT_STATUS: %s\n' "$status" | tee -a "$log"
  return "$status"
}

run_logged 07a-kompile-body-mutant-base \
  kompile verification-body-mutant.k \
  --backend haskell \
  --main-module MPY-BODY-MUTANT-BASE \
  --syntax-module MPY-SYNTAX \
  --output-definition body-mutant-base-kompiled || exit $?

run_logged 07b-kprove-body-mutant-aux \
  kprove spec-body-mutant.k \
  --definition body-mutant-base-kompiled \
  --spec-module AUX-BODY-MUTANT
aux_status=$?
if [[ $aux_status -eq 0 ]]; then
  printf 'BODY_SENSITIVITY_RESULT: invalid; changed-body connection theorem closed\n'
  exit 1
fi
if ! rg -q 'WarnStuckClaimState|cannot be rewritten further|implication check' \
  "$evidence/07b-kprove-body-mutant-aux.log"; then
  printf 'BODY_SENSITIVITY_RESULT: invalid; failure lacked semantic residual\n'
  exit 1
fi

run_logged 07c-kompile-body-mutant-lemma \
  kompile verification-body-mutant.k \
  --backend haskell \
  --main-module MPY-BODY-MUTANT-LEMMA \
  --syntax-module MPY-SYNTAX \
  --output-definition body-mutant-lemma-kompiled || exit $?

run_logged 07d-kprove-body-mutant-main \
  kprove spec-body-mutant.k \
  --definition body-mutant-lemma-kompiled \
  --spec-module MAIN-BODY-MUTANT || exit $?
if ! grep -qx '#Top' "$evidence/07d-kprove-body-mutant-main.log"; then
  printf 'BODY_SENSITIVITY_RESULT: main summary did not close as expected\n'
  exit 1
fi

printf '%s\n' \
  'BODY_SENSITIVITY_RESULT: the changed program invalidates the bridge-free auxiliary theorem; the admitted main-summary rule alone still closes, confirming that both submitted positive claims are essential.'
