#!/usr/bin/env bash
set -euo pipefail

work=/tmp/audit-work/candidate-clean
evidence=/audit-output/evidence

echo 'AUDIT COMMAND: bash /audit-output/evidence/stage3_reconstruct.sh'
echo 'PRECONDITION: scratch contains only copied K/Python sources, no candidate definitions or caches'
find "$work" -maxdepth 1 -printf '%f %y\n' | sort

echo 'COMMAND: python3 /audit-output/evidence/build_concrete_runner.py'
python3 "$evidence/build_concrete_runner.py"
echo 'COMMAND: python3 /tmp/audit-work/trusted/py2mpy.py concrete_runner.py > concrete_runner.mpy'
python3 \
  /tmp/audit-work/trusted/py2mpy.py \
  "$work/concrete_runner.py" \
  > "$work/concrete_runner.mpy"

echo 'COMMAND: kompile --backend llvm reference-semantics/semantics.k --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition runtime-audit-kompiled'
set +e
(
  cd "$work"
  kompile \
    --backend llvm \
    reference-semantics/semantics.k \
    --main-module MPY-KRUN \
    --syntax-module MPY-SYNTAX \
    --output-definition runtime-audit-kompiled
) 2>&1 | tee "$evidence/stage3_kompile_llvm.log"
status=${PIPESTATUS[0]}
set -e
echo "kompile_llvm_exit=$status"
test "$status" -eq 0

echo 'COMMAND: krun concrete_runner.mpy --definition runtime-audit-kompiled'
set +e
(
  cd "$work"
  krun concrete_runner.mpy --definition runtime-audit-kompiled
) 2>&1 | tee "$evidence/stage3_krun.log"
status=${PIPESTATUS[0]}
set -e
echo "krun_exit=$status"
test "$status" -eq 0
grep -A2 '<k>' "$evidence/stage3_krun.log" | grep -q '    .K'
grep -A2 '<exit-code>' "$evidence/stage3_krun.log" | grep -q '    0'
echo 'krun_final_k_empty=true'
echo 'krun_exit_code_cell_zero=true'

echo 'COMMAND: kompile --backend haskell verification.k --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition verification-audit-kompiled'
set +e
(
  cd "$work"
  kompile \
    --backend haskell \
    verification.k \
    --main-module VERIFICATION \
    --syntax-module MPY-SYNTAX \
    --output-definition verification-audit-kompiled
) 2>&1 | tee "$evidence/stage3_kompile_haskell.log"
status=${PIPESTATUS[0]}
set -e
echo "kompile_haskell_exit=$status"
test "$status" -eq 0

for claim in reverse-loop search-loop
do
  log="$evidence/stage3_kprove_${claim}.log"
  echo "COMMAND: kprove spec.k --definition verification-audit-kompiled --spec-module SPEC --claims SPEC.${claim}"
  set +e
  (
    cd "$work"
    kprove \
      spec.k \
      --definition verification-audit-kompiled \
      --spec-module SPEC \
      --claims "SPEC.${claim}"
  ) 2>&1 | tee "$log"
  status=${PIPESTATUS[0]}
  set -e
  echo "kprove_${claim}_exit=$status"
  top_count="$(grep -xc '#Top' "$log" || true)"
  echo "kprove_${claim}_top_count=$top_count"
  test "$status" -eq 0
  test "$top_count" -eq 1
done

echo 'DIAGNOSTIC COMMAND (dependency isolation): kprove spec.k --definition verification-audit-kompiled --spec-module SPEC --claims SPEC.make-palindrome-entry'
set +e
(
  cd "$work"
  kprove \
    spec.k \
    --definition verification-audit-kompiled \
    --spec-module SPEC \
    --claims SPEC.make-palindrome-entry
) 2>&1 | tee "$evidence/stage3_kprove_make-palindrome-entry.log"
status=${PIPESTATUS[0]}
set -e
echo "kprove_entry_without_loop_claims_exit=$status"
test "$status" -ne 0
grep -q 'WarnStuckClaimState' "$evidence/stage3_kprove_make-palindrome-entry.log"
echo 'entry_dependency_isolation_expected_failure=true'

echo 'COMMAND: kprove spec.k --definition verification-audit-kompiled --spec-module SPEC'
set +e
(
  cd "$work"
  kprove \
    spec.k \
    --definition verification-audit-kompiled \
    --spec-module SPEC
) 2>&1 | tee "$evidence/stage3_kprove_all.log"
status=${PIPESTATUS[0]}
set -e
echo "kprove_all_exit=$status"
top_count="$(grep -xc '#Top' "$evidence/stage3_kprove_all.log" || true)"
echo "kprove_all_top_count=$top_count"
test "$status" -eq 0
test "$top_count" -eq 1

echo 'STAGE3_RECONSTRUCTION_EXIT=0'
