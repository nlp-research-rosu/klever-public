#!/usr/bin/env bash
set -u

export PATH="$HOME/.nix-profile/bin:$PATH"
scratch=/tmp/audit-work/140-fix-spaces
evidence=/audit-output/evidence
overall=0

run_logged() {
  name=$1
  shift
  log="$evidence/$name.log"
  {
    printf '$'
    printf ' %q' "$@"
    printf '\n'
  } > "$log"
  "$@" >> "$log" 2>&1
  status=$?
  printf '[exit %d]\n' "$status" >> "$log"
  printf '%s exit=%d\n' "$name" "$status"
  if [[ "$status" -ne 0 ]]; then
    overall=1
  fi
}

cd "$scratch" || exit 2

run_logged reconstruct-01-python-tests \
  python3 concrete-tests.py

run_logged reconstruct-02-kompile-runtime \
  kompile reference-semantics/semantics.k \
    --backend llvm \
    --main-module MPY-KRUN \
    --syntax-module MPY-SYNTAX \
    --output-definition runtime-kompiled

run_logged reconstruct-03-krun-concrete-tests \
  krun concrete-tests.mpy \
    --definition runtime-kompiled

run_logged reconstruct-10-kompile-flush \
  kompile verification.k \
    --backend haskell \
    --main-module FIX-SPACES-BASE \
    --syntax-module MPY-SYNTAX \
    --output-definition proof-base-kompiled

for label in flush-zero flush-one flush-two flush-many; do
  run_logged "reconstruct-11-kprove-$label" \
    kprove spec.k \
      --definition proof-base-kompiled \
      --spec-module FIX-SPACES-FLUSH-SPEC \
      --claims "FIX-SPACES-FLUSH-SPEC.$label"
done

run_logged reconstruct-20-kompile-step \
  kompile verification.k \
    --backend haskell \
    --main-module FIX-SPACES-FLUSH-VERIFICATION \
    --syntax-module MPY-SYNTAX \
    --output-definition proof-step-kompiled

for label in step-space step-non-space; do
  run_logged "reconstruct-21-kprove-$label" \
    kprove spec.k \
      --definition proof-step-kompiled \
      --spec-module FIX-SPACES-STEP-SPEC \
      --claims "FIX-SPACES-STEP-SPEC.$label"
done

run_logged reconstruct-30-kompile-loop \
  kompile verification.k \
    --backend haskell \
    --main-module FIX-SPACES-STEP-VERIFICATION \
    --syntax-module MPY-SYNTAX \
    --output-definition proof-loop-kompiled

run_logged reconstruct-31-kprove-loop \
  kprove spec.k \
    --definition proof-loop-kompiled \
    --spec-module FIX-SPACES-LOOP-SPEC

run_logged reconstruct-40-kompile-main \
  kompile verification.k \
    --backend haskell \
    --main-module FIX-SPACES-VERIFICATION \
    --syntax-module MPY-SYNTAX \
    --output-definition proof-main-kompiled

run_logged reconstruct-41-kprove-main \
  kprove spec.k \
    --definition proof-main-kompiled \
    --spec-module FIX-SPACES-MAIN-SPEC

printf 'overall_exit=%d\n' "$overall"
exit "$overall"
