#!/usr/bin/env bash
set +e

source_dir=/tmp/audit-work/candidate-src
build_dir=/tmp/audit-work/build
evidence_dir=/audit-output/evidence
mkdir -p "$build_dir"

run_logged() {
  logfile=$1
  shift
  (
    printf '$'
    printf ' %q' "$@"
    printf '\n'
    "$@"
    rc=$?
    printf 'EXIT_STATUS=%d\n' "$rc"
    exit "$rc"
  ) 2>&1 | tee "$logfile"
  return "${PIPESTATUS[0]}"
}

cd "$source_dir" || exit 125

run_logged "$evidence_dir/stage3-tool-versions.log" bash -c \
  'kompile --version && kprove --version && krun --version'
versions_rc=$?

run_logged "$evidence_dir/stage3-runtime-build.log" \
  kompile reference-semantics/semantics.k \
    --backend llvm \
    --main-module MPY-KRUN \
    --syntax-module MPY-SYNTAX \
    --output-definition "$build_dir/runtime-kompiled"
runtime_rc=$?

run_logged "$evidence_dir/stage3-proof-build.log" \
  kompile verification.k \
    --backend haskell \
    --main-module VERIFICATION \
    --syntax-module MPY-SYNTAX \
    --output-definition "$build_dir/verification-kompiled"
proof_build_rc=$?

run_logged "$evidence_dir/stage3-claim-loop.log" \
  kprove spec.k \
    --definition "$build_dir/verification-kompiled" \
    --spec-module SPEC \
    --claims loop
claim_rc=$?

printf 'versions_rc=%d\n' "$versions_rc"
printf 'runtime_build_rc=%d\n' "$runtime_rc"
printf 'proof_build_rc=%d\n' "$proof_build_rc"
printf 'claim_loop_rc=%d\n' "$claim_rc"

if (( versions_rc != 0 || runtime_rc != 0 || proof_build_rc != 0 || claim_rc != 0 )); then
  exit 1
fi
exit 0
