#!/usr/bin/env bash
set -u

scratch="/tmp/audit-work/37-sort-even"
evidence="/audit-output/evidence"
summary="$evidence/03-reconstruction-summary.log"
runtime_def="$scratch/runtime-kompiled-fresh"
proof_def="$scratch/verification-kompiled-fresh"

printf '%s\n' \
  'Clean reconstruction uses only the scratch source copy and trusted supplied semantics.' \
  'No candidate-built definition or cache was copied.' \
  > "$summary"

run_logged() {
  name="$1"
  command_text="$2"
  shift 2
  log="$evidence/03-${name}.log"
  printf 'COMMAND: %s\n' "$command_text" > "$log"
  "$@" >> "$log" 2>&1
  status=$?
  printf 'EXIT_STATUS: %s\n' "$status" >> "$log"
  printf '%s_EXIT_STATUS: %s\n' "$name" "$status" >> "$summary"
  return "$status"
}

run_logged \
  toolchain \
  'kompile --version && krun --version && kprove --version' \
  bash -c 'kompile --version && krun --version && kprove --version'
toolchain_status=$?

printf '%s\n' \
  'COMMAND: cp -a /audit-output/evidence/k_concrete_tests.py /tmp/audit-work/37-sort-even/audit-concrete-tests.py' \
  > "$evidence/03-concrete-translate.log"
cp -a "$evidence/k_concrete_tests.py" "$scratch/audit-concrete-tests.py" \
  >> "$evidence/03-concrete-translate.log" 2>&1
copy_status=$?
if [ "$copy_status" -eq 0 ]; then
  printf '%s\n' \
    'COMMAND: python3 py2mpy.py audit-concrete-tests.py > audit-concrete-tests.mpy' \
    >> "$evidence/03-concrete-translate.log"
  (
    cd "$scratch" &&
    python3 py2mpy.py audit-concrete-tests.py > audit-concrete-tests.mpy
  ) >> "$evidence/03-concrete-translate.log" 2>&1
  translate_status=$?
else
  translate_status=1
fi
printf 'COPY_EXIT_STATUS: %s\nTRANSLATOR_EXIT_STATUS: %s\n' \
  "$copy_status" "$translate_status" >> "$evidence/03-concrete-translate.log"
printf 'concrete_translate_EXIT_STATUS: %s\n' "$translate_status" >> "$summary"

if [ "$toolchain_status" -eq 0 ] && [ "$translate_status" -eq 0 ]; then
  run_logged \
    llvm-build \
    'kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition runtime-kompiled-fresh' \
    bash -c "cd '$scratch' && kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition '$runtime_def'"
  llvm_status=$?
else
  llvm_status=1
fi

if [ "$llvm_status" -eq 0 ]; then
  run_logged \
    concrete-krun \
    'krun audit-concrete-tests.mpy --definition runtime-kompiled-fresh --output pretty' \
    bash -c "cd '$scratch' && krun audit-concrete-tests.mpy --definition '$runtime_def' --output pretty"
  krun_status=$?
else
  krun_status=1
fi

if [ "$toolchain_status" -eq 0 ]; then
  run_logged \
    haskell-build \
    'kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX -I . --output-definition verification-kompiled-fresh' \
    bash -c "cd '$scratch' && kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX -I . --output-definition '$proof_def'"
  haskell_status=$?
else
  haskell_status=1
fi

if [ "$haskell_status" -eq 0 ]; then
  run_logged \
    prove-loop \
    'kprove spec.k --definition verification-kompiled-fresh --spec-module SPEC --claims SPEC.loop-correct --output pretty' \
    bash -c "cd '$scratch' && kprove spec.k --definition '$proof_def' --spec-module SPEC --claims SPEC.loop-correct --output pretty"
  loop_status=$?

  run_logged \
    prove-entry \
    'kprove spec.k --definition verification-kompiled-fresh --spec-module SPEC --claims SPEC.loop-correct,SPEC.sort-even-correct --trusted SPEC.loop-correct --output pretty' \
    bash -c "cd '$scratch' && kprove spec.k --definition '$proof_def' --spec-module SPEC --claims SPEC.loop-correct,SPEC.sort-even-correct --trusted SPEC.loop-correct --output pretty"
  entry_status=$?
else
  loop_status=1
  entry_status=1
fi

for log in \
  "$evidence/03-toolchain.log" \
  "$evidence/03-concrete-translate.log" \
  "$evidence/03-llvm-build.log" \
  "$evidence/03-concrete-krun.log" \
  "$evidence/03-haskell-build.log" \
  "$evidence/03-prove-loop.log" \
  "$evidence/03-prove-entry.log"; do
  if [ -f "$log" ]; then
    sha256sum "$log" >> "$summary"
  fi
done

if [ "$toolchain_status" -ne 0 ] || [ "$translate_status" -ne 0 ] || \
   [ "$llvm_status" -ne 0 ] || [ "$krun_status" -ne 0 ] || \
   [ "$haskell_status" -ne 0 ] || [ "$loop_status" -ne 0 ] || \
   [ "$entry_status" -ne 0 ]; then
  printf '%s\n' 'OVERALL_EXIT_STATUS: 1' >> "$summary"
  exit 1
fi
printf '%s\n' 'OVERALL_EXIT_STATUS: 0' >> "$summary"
exit 0
