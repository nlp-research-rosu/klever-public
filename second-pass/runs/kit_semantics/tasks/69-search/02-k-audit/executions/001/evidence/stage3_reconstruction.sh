#!/usr/bin/env bash
set -uo pipefail
set -x

cd /tmp/audit-work/reconstruction
status=0

cp /audit-output/evidence/concrete_reconstruction.py concrete_reconstruction.py
python3 py2mpy.py concrete_reconstruction.py > concrete_reconstruction.mpy
translate_exit=$?
printf 'concrete_translation_exit=%s\n' "$translate_exit"
if [[ "$translate_exit" != 0 ]]; then
  status=1
fi

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled \
  2>&1 |
  tail -n 200 |
  tee /audit-output/evidence/stage3_llvm_compile_bounded.log
llvm_compile_exit="${PIPESTATUS[0]}"
printf 'llvm_compile_exit=%s\n' "$llvm_compile_exit"
if [[ "$llvm_compile_exit" != 0 ]]; then
  status=1
fi

if [[ "$llvm_compile_exit" == 0 ]]; then
  krun concrete_reconstruction.mpy \
    --definition audit-runtime-kompiled \
    2>&1 |
    tail -n 200 |
    tee /audit-output/evidence/stage3_krun_bounded.log
  krun_exit="${PIPESTATUS[0]}"
  printf 'krun_exit=%s\n' "$krun_exit"
  if [[ "$krun_exit" != 0 ]]; then
    status=1
  fi
else
  printf '%s\n' 'krun_skipped_due_to_compile_failure'
  status=1
fi

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled \
  2>&1 |
  tail -n 200 |
  tee /audit-output/evidence/stage3_haskell_compile_bounded.log
haskell_compile_exit="${PIPESTATUS[0]}"
printf 'haskell_compile_exit=%s\n' "$haskell_compile_exit"
if [[ "$haskell_compile_exit" != 0 ]]; then
  status=1
fi

if [[ "$haskell_compile_exit" == 0 ]]; then
  kprove spec.k \
    --definition audit-verification-kompiled \
    --spec-module SPEC \
    2>&1 |
    tail -n 200 |
    tee /audit-output/evidence/stage3_kprove_all_bounded.log
  all_claims_exit="${PIPESTATUS[0]}"
  printf 'all_claims_exit=%s\n' "$all_claims_exit"
  if [[ "$all_claims_exit" != 0 ]] ||
     ! grep -qx '#Top' /audit-output/evidence/stage3_kprove_all_bounded.log; then
    status=1
  fi
else
  printf '%s\n' 'kprove_skipped_due_to_compile_failure'
  status=1
fi

printf 'stage3_reconstruction_exit=%s\n' "$status"
exit "$status"
