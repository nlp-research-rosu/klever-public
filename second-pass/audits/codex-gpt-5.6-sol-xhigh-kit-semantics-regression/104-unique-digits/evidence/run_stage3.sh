#!/usr/bin/env bash
set -u

work=/tmp/audit-work
evidence=/audit-output/evidence
cd "$work" || exit 90

run_logged() {
  local name="$1"
  shift
  local log="$evidence/$name"
  echo "$ $*" | tee "$log"
  "$@" 2>&1 | tee -a "$log"
  local status=${PIPESTATUS[0]}
  echo "EXIT_STATUS=$status" | tee -a "$log"
  return "$status"
}

echo '$ python3 py2mpy.py /audit-output/evidence/concrete_harness.py > concrete_harness.mpy' \
  | tee "$evidence/03a-translate-concrete.log"
python3 py2mpy.py "$evidence/concrete_harness.py" > concrete_harness.mpy \
  2>> "$evidence/03a-translate-concrete.log"
translate_status=$?
echo "EXIT_STATUS=$translate_status" | tee -a "$evidence/03a-translate-concrete.log"
if [[ "$translate_status" -ne 0 ]]; then
  exit "$translate_status"
fi

run_logged 03b-kompile-llvm.log \
  kompile reference-semantics/semantics.k \
    --backend llvm \
    --main-module MPY-KRUN \
    --syntax-module MPY-SYNTAX \
    --output-definition audit-runtime-kompiled
llvm_build_status=$?
if [[ "$llvm_build_status" -ne 0 ]]; then
  exit "$llvm_build_status"
fi

run_logged 03c-krun-concrete.log \
  krun concrete_harness.mpy --definition audit-runtime-kompiled
krun_status=$?

run_logged 03d-kompile-verification-base.log \
  kompile --backend haskell verification.k \
    --main-module VERIFICATION \
    --syntax-module MPY-SYNTAX \
    --output-definition audit-verification-base-kompiled
base_build_status=$?
if [[ "$base_build_status" -ne 0 ]]; then
  exit "$base_build_status"
fi

run_logged 03e-kprove-loop.log \
  kprove spec.k \
    --definition audit-verification-base-kompiled \
    --spec-module LOOP-SPEC \
    --claims LOOP-SPEC.outer-loop
loop_status=$?

run_logged 03f-kompile-verification-full.log \
  kompile --backend haskell verification.k \
    --main-module VERIFICATION-WITH-LOOP \
    --syntax-module MPY-SYNTAX \
    --output-definition audit-verification-kompiled
full_build_status=$?
if [[ "$full_build_status" -ne 0 ]]; then
  exit "$full_build_status"
fi

run_logged 03g-kprove-entry.log \
  kprove spec.k \
    --definition audit-verification-kompiled \
    --spec-module SPEC \
    --claims SPEC.entry
entry_status=$?

echo "SUMMARY translate=$translate_status llvm_build=$llvm_build_status krun=$krun_status " \
     "base_build=$base_build_status loop=$loop_status full_build=$full_build_status entry=$entry_status"

if [[ "$krun_status" -ne 0 || "$loop_status" -ne 0 || "$entry_status" -ne 0 ]]; then
  exit 1
fi
exit 0
