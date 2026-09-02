#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/reconstruction
evidence=/audit-output/evidence
overall=0

run_logged() {
  local label=$1
  shift
  echo "\$ $*"
  "$@" 2>&1 | tee "$evidence/$label.log"
  local status=${PIPESTATUS[0]}
  echo "EXIT_STATUS=$status" | tee -a "$evidence/$label.log"
  if (( status != 0 )); then
    overall=1
  fi
}

cd "$scratch" || exit 2

echo '$ tool versions'
kompile --version
kprove --version
python3 --version

run_logged 03a_kompile_concrete \
  kompile reference-semantics/semantics.k \
    --backend llvm \
    --main-module MPY-KRUN \
    --syntax-module MPY-SYNTAX \
    --output-definition audit-runtime-kompiled \
    --warnings none

run_logged 03b_krun_solution_module \
  krun solution.mpy \
    --definition audit-runtime-kompiled \
    --output pretty

run_logged 03c_kompile_proof \
  kompile verification.k \
    --backend haskell \
    --main-module CIRCULAR-SHIFT-VERIFICATION \
    --syntax-module MPY-SYNTAX \
    --output-definition audit-verification-kompiled \
    --warnings none

run_logged 03d_kprove_normal \
  kprove spec.k \
    --definition audit-verification-kompiled \
    --spec-module CIRCULAR-SHIFT-SPEC \
    --claims CIRCULAR-SHIFT-SPEC.normal-shift \
    --depth 300 \
    --warnings none

run_logged 03e_kprove_oversize \
  kprove spec.k \
    --definition audit-verification-kompiled \
    --spec-module CIRCULAR-SHIFT-SPEC \
    --claims CIRCULAR-SHIFT-SPEC.oversize-shift \
    --depth 300 \
    --warnings none

run_logged 03f_kprove_combined \
  kprove spec.k \
    --definition audit-verification-kompiled \
    --spec-module CIRCULAR-SHIFT-SPEC \
    --depth 300 \
    --warnings none

echo "OVERALL_EXIT_STATUS=$overall"
exit "$overall"
