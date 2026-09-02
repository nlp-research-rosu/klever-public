#!/usr/bin/env bash
set -o pipefail

scratch=/tmp/audit-work/source
llvm_definition=/tmp/audit-work/rebuilt-runtime-kompiled
haskell_definition=/tmp/audit-work/rebuilt-verification-kompiled

cd "$scratch" || exit 90

for definition in "$llvm_definition" "$haskell_definition"; do
  if test -e "$definition"; then
    echo "REFUSING_NONFRESH_DEFINITION=$definition"
    exit 91
  fi
done

echo '$ kompile --version'
kompile --version
echo "EXIT_STATUS=$?"
echo '$ kprove --version'
kprove --version
echo "EXIT_STATUS=$?"

{
  echo '$ python3 /reference/py2mpy.py /audit-output/evidence/concrete_reconstruction.py > /tmp/audit-work/source/concrete_reconstruction.mpy'
  python3 /reference/py2mpy.py \
    /audit-output/evidence/concrete_reconstruction.py \
    > /tmp/audit-work/source/concrete_reconstruction.mpy
  status=$?
  echo "EXIT_STATUS=$status"
  exit "$status"
} 2>&1 | tee /audit-output/evidence/translate_concrete.log
translate_status=${PIPESTATUS[0]}

{
  echo '$ kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition /tmp/audit-work/rebuilt-runtime-kompiled'
  kompile reference-semantics/semantics.k \
    --backend llvm \
    --main-module MPY-KRUN \
    --syntax-module MPY-SYNTAX \
    --output-definition "$llvm_definition"
  status=$?
  echo "EXIT_STATUS=$status"
  exit "$status"
} 2>&1 | tee /audit-output/evidence/kompile_llvm.log
llvm_status=${PIPESTATUS[0]}

{
  echo '$ krun concrete_reconstruction.mpy --definition /tmp/audit-work/rebuilt-runtime-kompiled'
  krun concrete_reconstruction.mpy --definition "$llvm_definition"
  status=$?
  echo "EXIT_STATUS=$status"
  exit "$status"
} 2>&1 | tee /audit-output/evidence/krun_concrete.log
krun_status=${PIPESTATUS[0]}

{
  echo '$ kompile --backend haskell verification.k --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition /tmp/audit-work/rebuilt-verification-kompiled'
  kompile --backend haskell verification.k \
    --main-module VERIFICATION \
    --syntax-module MPY-SYNTAX \
    --output-definition "$haskell_definition"
  status=$?
  echo "EXIT_STATUS=$status"
  exit "$status"
} 2>&1 | tee /audit-output/evidence/kompile_haskell.log
haskell_status=${PIPESTATUS[0]}

{
  echo '$ kprove spec.k --definition /tmp/audit-work/rebuilt-verification-kompiled --spec-module SPEC --claims SPEC.digits-loop'
  kprove spec.k \
    --definition "$haskell_definition" \
    --spec-module SPEC \
    --claims SPEC.digits-loop
  status=$?
  echo "EXIT_STATUS=$status"
  exit "$status"
} 2>&1 | tee /audit-output/evidence/kprove_digits_loop.log
loop_status=${PIPESTATUS[0]}

{
  echo '$ kprove spec.k --definition /tmp/audit-work/rebuilt-verification-kompiled --spec-module SPEC --claims SPEC.digits-entry'
  kprove spec.k \
    --definition "$haskell_definition" \
    --spec-module SPEC \
    --claims SPEC.digits-entry
  status=$?
  echo "EXIT_STATUS=$status"
  exit "$status"
} 2>&1 | tee /audit-output/evidence/kprove_digits_entry.log
entry_status=${PIPESTATUS[0]}

{
  echo '$ kprove spec.k --definition /tmp/audit-work/rebuilt-verification-kompiled --spec-module SPEC'
  kprove spec.k \
    --definition "$haskell_definition" \
    --spec-module SPEC
  status=$?
  echo "EXIT_STATUS=$status"
  exit "$status"
} 2>&1 | tee /audit-output/evidence/kprove_all.log
all_status=${PIPESTATUS[0]}

echo \
  "SUMMARY translate=$translate_status llvm=$llvm_status krun=$krun_status" \
  "haskell=$haskell_status loop=$loop_status entry=$entry_status all=$all_status"

test "$translate_status" -eq 0 \
  && test "$llvm_status" -eq 0 \
  && test "$krun_status" -eq 0 \
  && test "$haskell_status" -eq 0 \
  && test "$loop_status" -eq 0 \
  && test "$entry_status" -eq 0 \
  && test "$all_status" -eq 0
