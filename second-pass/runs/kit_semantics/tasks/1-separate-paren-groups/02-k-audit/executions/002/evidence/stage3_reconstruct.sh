#!/usr/bin/env bash
set -u

SCRATCH=/tmp/audit-work/reconstruction
EVIDENCE=/audit-output/evidence
overall=0

run_bounded() {
  local label="$1"
  local command_text="$2"
  local temporary
  temporary="$(mktemp /tmp/audit-work/${label}.XXXXXX)"

  printf '$ %s\n' "$command_text" > "$EVIDENCE/${label}.log"
  bash -o pipefail -c "$command_text" > "$temporary" 2>&1
  local status=$?
  local lines
  lines="$(wc -l < "$temporary")"
  local bytes
  bytes="$(wc -c < "$temporary")"
  printf '[captured output: %s lines, %s bytes]\n' "$lines" "$bytes" >> "$EVIDENCE/${label}.log"
  if [ "$lines" -le 500 ]; then
    sed -n '1,500p' "$temporary" >> "$EVIDENCE/${label}.log"
  else
    sed -n '1,80p' "$temporary" >> "$EVIDENCE/${label}.log"
    printf '[... bounded omission of middle output ...]\n' >> "$EVIDENCE/${label}.log"
    tail -n 420 "$temporary" >> "$EVIDENCE/${label}.log"
  fi
  printf '[exit %d]\n' "$status" >> "$EVIDENCE/${label}.log"
  rm -f "$temporary"
  printf '%s exit=%d log=%s/%s.log\n' "$label" "$status" "$EVIDENCE" "$label"
  if [ "$status" -ne 0 ]; then
    overall=1
  fi
}

run_bounded stage3_llvm_build \
  "cd '$SCRATCH' && kompile --backend llvm reference-semantics/semantics.k --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition audit-runtime-kompiled"

run_bounded stage3_solution_krun \
  "cd '$SCRATCH' && krun regenerated-solution.mpy --definition audit-runtime-kompiled"

run_bounded stage3_haskell_build \
  "cd '$SCRATCH' && kompile --backend haskell verification.k --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition audit-verification-kompiled"

run_bounded stage3_loop_claim \
  "cd '$SCRATCH' && kprove spec.k --definition audit-verification-kompiled --spec-module SPEC --claims SPEC.loop-invariant"

run_bounded stage3_function_claim \
  "cd '$SCRATCH' && kprove spec.k --definition audit-verification-kompiled --spec-module SPEC --claims SPEC.function-correct"

run_bounded stage3_all_claims \
  "cd '$SCRATCH' && kprove spec.k --definition audit-verification-kompiled --spec-module SPEC"

exit "$overall"
