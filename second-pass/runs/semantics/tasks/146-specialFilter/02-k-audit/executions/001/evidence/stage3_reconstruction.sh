#!/usr/bin/env bash
set -u
set -o pipefail
set -x

PATH="/home/agent/.nix-profile/bin:$PATH"
work=${AUDIT_WORK_DIR:-/tmp/audit-work/candidate-clean}
evidence=/audit-output/evidence
overall=0

command -v kompile
command -v kprove
command -v krun
kompile --version
kprove --version
krun --version

python3 /reference/py2mpy.py "$evidence/k_concrete_audit.py" \
  > "$work/k-concrete-audit.mpy"
status=$?
printf 'CONCRETE_TRANSLATE_EXIT=%s\n' "$status"
(( status == 0 )) || overall=1

kompile "$work/reference-semantics/semantics.k" \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition "$work/runtime-kompiled" \
  2>&1 | tee "$evidence/stage3_llvm_build.log"
status=${PIPESTATUS[0]}
printf 'LLVM_BUILD_EXIT=%s\n' "$status"
(( status == 0 )) || overall=1

if (( status == 0 )); then
  krun "$work/k-concrete-audit.mpy" \
    --definition "$work/runtime-kompiled" \
    --output pretty \
    2>&1 | tee "$evidence/stage3_concrete_krun.log"
  status=${PIPESTATUS[0]}
  printf 'CONCRETE_KRUN_EXIT=%s\n' "$status"
  (( status == 0 )) || overall=1
  if ! grep -q 'NoExc' "$evidence/stage3_concrete_krun.log"; then
    printf 'CONCRETE_EXPECTED_NOEXC_NOT_FOUND\n'
    overall=1
  fi
fi

kompile "$work/verification.k" \
  --backend haskell \
  --main-module SPECIALFILTER-VERIFICATION-LOOP \
  --syntax-module MPY-SYNTAX \
  --output-definition "$work/loop-kompiled" \
  2>&1 | tee "$evidence/stage3_loop_build.log"
status=${PIPESTATUS[0]}
printf 'LOOP_BUILD_EXIT=%s\n' "$status"
(( status == 0 )) || overall=1

if (( status == 0 )); then
  kprove "$work/spec.k" \
    --definition "$work/loop-kompiled" \
    --spec-module SPECIALFILTER-LOOP-SPEC \
    2>&1 | tee "$evidence/stage3_loop_proof.log"
  status=${PIPESTATUS[0]}
  printf 'LOOP_PROOF_EXIT=%s\n' "$status"
  (( status == 0 )) || overall=1
  if ! grep -qx '#Top' "$evidence/stage3_loop_proof.log"; then
    printf 'LOOP_PROOF_EXACT_TOP_NOT_FOUND\n'
    overall=1
  fi
fi

kompile "$work/verification.k" \
  --backend haskell \
  --main-module SPECIALFILTER-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition "$work/verification-kompiled" \
  2>&1 | tee "$evidence/stage3_call_build.log"
status=${PIPESTATUS[0]}
printf 'CALL_BUILD_EXIT=%s\n' "$status"
(( status == 0 )) || overall=1

if (( status == 0 )); then
  kprove "$work/spec.k" \
    --definition "$work/verification-kompiled" \
    --spec-module SPECIALFILTER-SPEC \
    2>&1 | tee "$evidence/stage3_call_proof.log"
  status=${PIPESTATUS[0]}
  printf 'CALL_PROOF_EXIT=%s\n' "$status"
  (( status == 0 )) || overall=1
  if ! grep -qx '#Top' "$evidence/stage3_call_proof.log"; then
    printf 'CALL_PROOF_EXACT_TOP_NOT_FOUND\n'
    overall=1
  fi
fi

printf 'STAGE3_OVERALL_EXIT=%s\n' "$overall"
exit "$overall"
