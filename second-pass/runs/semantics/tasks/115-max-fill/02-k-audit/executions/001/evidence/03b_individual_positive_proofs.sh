#!/usr/bin/env bash
set -u
set -o pipefail

WORK=/tmp/audit-work/115-max-fill
overall=0

run() {
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf 'EXIT_STATUS: %s\n\n' "$status"
  if [[ "$status" -ne 0 ]]; then
    overall=1
  fi
  return 0
}

cd "$WORK" || exit 125
export PATH="$HOME/.nix-profile/bin:$PATH"

printf '%s\n' '## Every bridge claim selected independently'
for label in \
  MAX-FILL-BRIDGE-SPEC.bridge-sum-empty \
  MAX-FILL-BRIDGE-SPEC.bridge-sum-step \
  MAX-FILL-BRIDGE-SPEC.bridge-loop-empty \
  MAX-FILL-BRIDGE-SPEC.bridge-loop-step
do
  run timeout 300s kprove spec.k \
    --definition bridge-check-kompiled \
    --spec-module MAX-FILL-BRIDGE-SPEC \
    --claims "$label"
done

printf '%s\n' '## Each main target with necessary preceding auxiliaries'
run timeout 300s kprove spec.k \
  --definition verification-kompiled \
  --spec-module MAX-FILL-SPEC \
  --claims MAX-FILL-SPEC.sum-fold
run timeout 450s kprove spec.k \
  --definition verification-kompiled \
  --spec-module MAX-FILL-SPEC \
  --claims MAX-FILL-SPEC.sum-fold,MAX-FILL-SPEC.fill-loop
run timeout 600s kprove spec.k \
  --definition verification-kompiled \
  --spec-module MAX-FILL-SPEC \
  --claims MAX-FILL-SPEC.sum-fold,MAX-FILL-SPEC.fill-loop,MAX-FILL-SPEC.max-fill-correct

exit "$overall"
