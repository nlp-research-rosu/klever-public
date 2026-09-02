#!/usr/bin/env bash
set -u

export PATH="/home/agent/.nix-profile/bin:$PATH"
evidence_dir=/audit-output/evidence
scratch_dir=/tmp/audit-work

run_capture() {
  local label=$1
  shift
  local logfile="$evidence_dir/$label.log"
  printf '$' | tee "$logfile"
  printf ' %q' "$@" | tee -a "$logfile"
  printf '\n' | tee -a "$logfile"
  "$@" 2>&1 | tee -a "$logfile"
  local rc=${PIPESTATUS[0]}
  printf '[exit %d]\n' "$rc" | tee -a "$logfile"
  return "$rc"
}

cd "$scratch_dir" || exit 1

overall=0

echo "## Clean-state checks"
for definition in runtime-kompiled verification-kompiled; do
  printf '$ test ! -e %s\n' "$definition"
  test ! -e "$definition"
  rc=$?
  printf '[exit %d]\n' "$rc"
  (( rc == 0 )) || overall=1
done

echo "## K tool versions"
run_capture stage3_kompile_version kompile --version || overall=1
run_capture stage3_kprove_version kprove --version || overall=1
run_capture stage3_krun_version krun --version || overall=1

echo "## Fresh LLVM semantics build"
run_capture stage3_llvm_build \
  kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled || overall=1

echo "## Concrete execution"
run_capture stage3_concrete_tests \
  krun concrete-tests.mpy \
  --definition runtime-kompiled || overall=1

echo "## Fresh Haskell proof-definition build"
run_capture stage3_haskell_build \
  kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled || overall=1

echo "## Positive target claims"
run_capture stage3_prefix_proof \
  kprove spec.k \
  --definition verification-kompiled \
  --spec-module PREFIX-SPEC || overall=1

run_capture stage3_init_proof \
  kprove spec.k \
  --definition verification-kompiled \
  --spec-module INIT-SPEC || overall=1

run_capture stage3_loop_proof \
  kprove spec.k \
  --definition verification-kompiled \
  --spec-module LOOP-SPEC || overall=1

exit "$overall"
