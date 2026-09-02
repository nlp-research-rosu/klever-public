#!/usr/bin/env bash
set -u

work=/tmp/audit-work/body-mutation

run() {
  printf '+'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf 'EXIT_STATUS=%d\n' "$status"
  return "$status"
}

run nl -ba "$work/solution-program.k"
run kompile "$work/verification.k" \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition "$work/proof-kompiled"
build_status=$?
if (( build_status != 0 )); then
  exit "$build_status"
fi

printf '+ kprove %q --definition %q --spec-module SPEC-LABELED --claims SPEC-LABELED.universal\n' \
  "$work/spec-labeled.k" "$work/proof-kompiled"
kprove "$work/spec-labeled.k" \
  --definition "$work/proof-kompiled" \
  --spec-module SPEC-LABELED \
  --claims SPEC-LABELED.universal
proof_status=$?
printf 'EXIT_STATUS=%d\n' "$proof_status"
printf 'EXPECTED_NONZERO=%s\n' "$([[ $proof_status -ne 0 ]] && printf yes || printf no)"

run krun "$work/solution.mpy" \
  --definition /tmp/audit-work/reconstruction/semantic-kompiled \
  '-cS0=""' '-cS1="a"'
printf 'NOTE=The krun command above executes the unmutated submitted solution.mpy; Python and K both return false for this witness.\n'
printf 'NOTE=The mutated solutionProgram instead compares set(s0) with itself and therefore yields true for S0="", S1="a".\n'

if (( proof_status == 0 )); then
  exit 1
fi
exit 0
