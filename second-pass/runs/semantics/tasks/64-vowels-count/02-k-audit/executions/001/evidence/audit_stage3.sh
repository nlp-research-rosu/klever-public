#!/usr/bin/env bash
set -u
set -o pipefail

EVIDENCE_DIR=/audit-output/evidence
WORK_DIR=/tmp/audit-work/fresh
export PATH="$HOME/.nix-profile/bin:$PATH"

run_logged() {
  log_name=$1
  shift
  log_path="$EVIDENCE_DIR/$log_name"
  {
    printf '$'
    printf ' %q' "$@"
    printf '\n'
  } | tee "$log_path"
  "$@" 2>&1 | tee -a "$log_path"
  status=${PIPESTATUS[0]}
  printf '[exit %d]\n' "$status" | tee -a "$log_path"
  return 0
}

cd "$WORK_DIR" || exit 1

run_logged stage3-kompile-runtime.log \
  kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

run_logged stage3-kompile-proof-base.log \
  kompile verification.k \
  --backend haskell \
  --main-module VOWELS-BASE \
  --syntax-module MPY-SYNTAX \
  --output-definition proof-base-kompiled

run_logged stage3-kprove-loop.log \
  kprove spec.k \
  --definition proof-base-kompiled \
  --spec-module LOOP-SPEC \
  --output pretty

run_logged stage3-kompile-verification.log \
  kompile verification.k \
  --backend haskell \
  --main-module VOWELS-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

run_logged stage3-kprove-main.log \
  kprove spec.k \
  --definition verification-kompiled \
  --spec-module MAIN-SPEC \
  --output pretty
