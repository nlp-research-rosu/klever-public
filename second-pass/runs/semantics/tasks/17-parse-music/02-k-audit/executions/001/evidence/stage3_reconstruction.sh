#!/usr/bin/env bash
set -u
set -o pipefail
set -x

work=/tmp/audit-work/reconstruction
cd "$work" || exit 90

kompile --version
kprove --version
krun --version

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
runtime_build_status=$?
printf 'runtime kompile exit: %d\n' "$runtime_build_status"

if test "$runtime_build_status" -eq 0; then
  krun concrete-test.mpy --definition runtime-kompiled
  concrete_status=$?
else
  concrete_status=125
fi
printf 'concrete-test krun exit: %d\n' "$concrete_status"

kompile verification.k \
  --backend haskell \
  --main-module PARSE-MUSIC-BASE \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-base-kompiled
base_build_status=$?
printf 'base proof kompile exit: %d\n' "$base_build_status"

if test "$base_build_status" -eq 0; then
  kprove spec.k \
    --definition verification-base-kompiled \
    --spec-module PARSE-MUSIC-LOOP-SPEC
  loop_proof_status=$?
else
  loop_proof_status=125
fi
printf 'loop claim kprove exit: %d\n' "$loop_proof_status"

kompile verification.k \
  --backend haskell \
  --main-module PARSE-MUSIC-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
entry_build_status=$?
printf 'entry proof kompile exit: %d\n' "$entry_build_status"

if test "$entry_build_status" -eq 0; then
  kprove spec.k \
    --definition verification-kompiled \
    --spec-module PARSE-MUSIC-ENTRY-SPEC \
    --branching-allowed 100
  entry_proof_status=$?
else
  entry_proof_status=125
fi
printf 'entry claim kprove exit: %d\n' "$entry_proof_status"

if test "$runtime_build_status" -ne 0 \
  || test "$concrete_status" -ne 0 \
  || test "$base_build_status" -ne 0 \
  || test "$loop_proof_status" -ne 0 \
  || test "$entry_build_status" -ne 0 \
  || test "$entry_proof_status" -ne 0; then
  exit 1
fi
exit 0
