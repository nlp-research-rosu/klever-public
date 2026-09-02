#!/usr/bin/env bash
set -uo pipefail

log=/audit-output/evidence/stage3_clean_reconstruction.log
scratch=/tmp/audit-work/review-34-unique
exec >"$log" 2>&1
cd "$scratch" || exit 99

run() {
  echo "COMMAND: $*"
  "$@"
  status=$?
  echo "EXIT: $status"
  return "$status"
}

echo "STAGE 3 CLEAN PROOF RECONSTRUCTION"
run kompile --version || exit $?
run kprove --version || exit $?
run krun --version || exit $?

echo "COMMAND: confirm no candidate-built definition existed in the scratch copy before rebuilding"
find . -maxdepth 1 -type d -name '*-kompiled' -print
status=$?
echo "EXIT: $status"

run kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled || exit $?

run krun smoke.mpy --definition audit-runtime-kompiled || exit $?

run kompile --backend haskell verification.k \
  --main-module VERIFICATION-BASE \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-base-kompiled || exit $?

run kprove spec.k \
  --definition audit-verification-base-kompiled \
  --spec-module MEMBER-SPEC || exit $?

run kompile --backend haskell verification.k \
  --main-module VERIFICATION-MEMBER \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-member-kompiled || exit $?

run kprove spec.k \
  --definition audit-verification-member-kompiled \
  --spec-module LOOP-SPEC || exit $?

run kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled || exit $?

run kprove spec.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC || exit $?

run kprove bridge-probes.k \
  --definition audit-verification-base-kompiled \
  --spec-module MEMBER-PROBE-BASE || exit $?

run kprove bridge-probes.k \
  --definition audit-verification-member-kompiled \
  --spec-module MEMBER-PROBE-BRIDGED || exit $?

run kprove bridge-probes.k \
  --definition audit-verification-member-kompiled \
  --spec-module LOOP-PROBE-FIXED || exit $?

run kprove bridge-probes.k \
  --definition audit-verification-kompiled \
  --spec-module LOOP-PROBE-BRIDGED || exit $?

run kprove model-boundary.k \
  --definition audit-verification-base-kompiled \
  --spec-module MODEL-BOUNDARY || exit $?

echo "COMMAND: count exact successful #Top lines"
grep -c '^#Top$' "$log"
status=$?
echo "EXIT: $status"
