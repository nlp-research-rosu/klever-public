#!/usr/bin/env bash
set -u

SCRATCH=/tmp/audit-work/reconstruction
EVIDENCE=/audit-output/evidence/logs
export PATH="/home/agent/.nix-profile/bin:$PATH"

run_bounded() {
  name=$1
  shift
  full="$SCRATCH/$name.full.log"
  bounded="$EVIDENCE/$name.log"
  {
    printf '$'
    printf ' %q' "$@"
    printf '\n'
  } > "$bounded"
  "$@" > "$full" 2>&1
  status=$?
  lines=$(wc -l < "$full")
  {
    printf '[exit %d; output lines %d]\n' "$status" "$lines"
    if [ "$lines" -le 200 ]; then
      sed -n '1,200p' "$full"
    else
      sed -n '1,100p' "$full"
      printf '[... %d middle lines omitted ...]\n' "$((lines - 200))"
      tail -n 100 "$full"
    fi
  } >> "$bounded"
  sed -n '1,220p' "$bounded"
  return "$status"
}

cd "$SCRATCH" || exit 1

run_bounded k_version kompile --version || exit $?

# These output paths did not exist in the clean scratch copy.
run_bounded build_runtime \
  kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled || exit $?

run_bounded build_verification_base \
  kompile --backend haskell verification.k \
  --main-module VERIFICATION-BASE --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-base-kompiled || exit $?

run_bounded prove_loop_spec \
  kprove spec.k --definition audit-verification-base-kompiled \
  --spec-module LOOP-SPEC || exit $?

run_bounded prove_entry_spec \
  kprove spec.k --definition audit-verification-base-kompiled \
  --spec-module SPEC || exit $?

run_bounded build_verification_bridge \
  kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled || exit $?

run_bounded prove_for_spec \
  kprove spec.k --definition audit-verification-kompiled \
  --spec-module FOR-SPEC || exit $?
