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

printf '%s\n' '## Toolchain'
run kompile --version
run kprove --version

printf '%s\n' '## Fresh concrete definition and execution'
run timeout 600s kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
run timeout 180s krun concrete-tests.mpy --definition runtime-kompiled

printf '%s\n' '## Fresh bridge-check definition'
run timeout 600s kompile verification.k \
  --backend haskell \
  --main-module MAX-FILL-DATA \
  --syntax-module MPY-SYNTAX \
  --output-definition bridge-check-kompiled

printf '%s\n' '## Bridge claims together'
run timeout 300s kprove spec.k \
  --definition bridge-check-kompiled \
  --spec-module MAX-FILL-BRIDGE-SPEC

printf '%s\n' '## Every bridge claim selected independently'
for label in bridge-sum-empty bridge-sum-step bridge-loop-empty bridge-loop-step; do
  run timeout 300s kprove spec.k \
    --definition bridge-check-kompiled \
    --spec-module MAX-FILL-BRIDGE-SPEC \
    --claims "$label"
done

printf '%s\n' '## Fresh full verification definition'
run timeout 600s kompile verification.k \
  --backend haskell \
  --main-module MAX-FILL-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

printf '%s\n' '## Main claims together'
run timeout 600s kprove spec.k \
  --definition verification-kompiled \
  --spec-module MAX-FILL-SPEC

printf '%s\n' '## Main claims, each target with only its required auxiliaries'
run timeout 300s kprove spec.k \
  --definition verification-kompiled \
  --spec-module MAX-FILL-SPEC \
  --claims sum-fold
run timeout 450s kprove spec.k \
  --definition verification-kompiled \
  --spec-module MAX-FILL-SPEC \
  --claims sum-fold,fill-loop
run timeout 600s kprove spec.k \
  --definition verification-kompiled \
  --spec-module MAX-FILL-SPEC \
  --claims sum-fold,fill-loop,max-fill-correct

exit "$overall"
