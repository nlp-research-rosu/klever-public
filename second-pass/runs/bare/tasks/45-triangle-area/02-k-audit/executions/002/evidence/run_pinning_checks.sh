#!/usr/bin/env bash
set -u

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

run python3 /audit-output/evidence/constructor_compare.py || exit 1

cd /tmp/audit-work/candidate || exit 1
run kompile verification-body-mutation.k \
  --backend haskell \
  --main-module VERIFICATION-BODY-MUTATION \
  --syntax-module TINY-PYTHON-SYNTAX \
  --output-definition body-mutation-kompiled || exit 1

printf '%s\n' '$ kprove spec-body-mutation.k --definition body-mutation-kompiled --spec-module SPEC-BODY-MUTATION'
proof_output="$(
  kprove spec-body-mutation.k \
    --definition body-mutation-kompiled \
    --spec-module SPEC-BODY-MUTATION 2>&1
)"
proof_status=$?
printf '%s\n' "$proof_output"
printf '[exit %d]\n' "$proof_status"
if (( proof_status == 0 )); then
  printf '%s\n' 'ERROR: divisor-3 body mutation unexpectedly proved'
  exit 1
fi
if [[ "$proof_output" != *WarnStuckClaimState* ]]; then
  printf '%s\n' 'ERROR: mutation failed for a reason other than a stuck claim'
  exit 1
fi
printf '%s\n' 'EXPECTED: the executed-body mutation invalidates the original result obligation'
