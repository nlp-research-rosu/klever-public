#!/usr/bin/env bash
set -u

SCRATCH=$(mktemp -d /tmp/audit-work/reconstruction-final.XXXXXX)
SOURCE="$SCRATCH/source"
CONCRETE_DEF="$SCRATCH/semantic-llvm"
PROOF_DEF="$SCRATCH/verification-haskell"

run_shell() {
  local command_text="$1"
  printf 'COMMAND: %s\n' "$command_text"
  bash -o pipefail -c "$command_text"
  local status=$?
  printf 'EXIT_STATUS: %s\n\n' "$status"
  return "$status"
}

printf 'CLEAN-ROOM SOURCE CHECK\n'
run_shell "mkdir -p '$SOURCE'"
run_shell "cp /tmp/audit-work/source/semantic.k /tmp/audit-work/source/solution.py /tmp/audit-work/source/solution.mpy /tmp/audit-work/source/spec.k /tmp/audit-work/source/verification.k '$SOURCE/'"
run_shell "test ! -e '$SOURCE/semantic-kompiled' -a ! -e '$SOURCE/verification-kompiled'"
run_shell "find '$SOURCE' -maxdepth 1 -type f -printf '%f %s bytes\n' | sort"
run_shell "kompile --version && kprove --version && krun --version"
run_shell "cp /audit-output/evidence/stage3/spec-labeled.k '$SOURCE/spec-labeled.k'"

printf 'FRESH CONCRETE DEFINITION BUILD\n'
run_shell "kompile '$SOURCE/semantic.k' --main-module SEMANTIC --syntax-module MPY-SYNTAX --backend llvm --output-definition '$CONCRETE_DEF'"
concrete_build_status=$?
if [[ $concrete_build_status -ne 0 ]]; then
  exit "$concrete_build_status"
fi

printf 'GENERATED-SEMANTICS CONCRETE EXECUTIONS\n'
overall=0
for n in -100 -1 0 1 50 78 79 118 144 771 7778; do
  command_text="krun '$SOURCE/solution.mpy' -cN=$n --definition '$CONCRETE_DEF'"
  printf 'COMMAND: %s\n' "$command_text"
  output=$(krun "$SOURCE/solution.mpy" -cN="$n" --definition "$CONCRETE_DEF" 2>&1)
  status=$?
  printf '%s\n' "$output"
  printf 'EXIT_STATUS: %s\n' "$status"
  actual=$(printf '%s\n' "$output" | awk '/<result>/{getline; gsub(/[[:space:]]/, ""); print; exit}')
  printf 'K_RESULT: %s\n' "$actual"
  python3 /audit-output/evidence/stage3/compare_concrete.py "$n"
  python_status=$?
  expected=$(python3 /audit-output/evidence/stage3/compare_concrete.py "$n" | awk '/PYTHON_CANONICAL:/{print $2}')
  if [[ $status -ne 0 || $python_status -ne 0 || "$actual" != "$expected" ]]; then
    printf 'CONCRETE_COMPARISON: MISMATCH\n\n'
    overall=1
  else
    printf 'CONCRETE_COMPARISON: MATCH\n\n'
  fi
done

printf 'FRESH PROOF DEFINITION BUILD\n'
run_shell "kompile '$SOURCE/verification.k' --main-module VERIFICATION --syntax-module MPY-SYNTAX --backend haskell --output-definition '$PROOF_DEF'"
proof_build_status=$?
if [[ $proof_build_status -ne 0 ]]; then
  exit "$proof_build_status"
fi

printf 'ORIGINAL MULTI-CLAIM PROOF\n'
run_shell "cd '$SOURCE' && kprove spec.k --definition '$PROOF_DEF' --spec-module SPEC"
all_claims_status=$?

printf 'INDIVIDUALLY SELECTED POSITIVE CLAIMS\n'
run_shell "cd '$SOURCE' && timeout 60s kprove spec-labeled.k --definition '$PROOF_DEF' --spec-module SPEC-LABELED --exclude SPEC-LABELED.outer,SPEC-LABELED.entry"
inner_status=$?
run_shell "cd '$SOURCE' && timeout 60s kprove spec-labeled.k --definition '$PROOF_DEF' --spec-module SPEC-LABELED --exclude SPEC-LABELED.entry --trusted SPEC-LABELED.inner"
outer_status=$?
run_shell "cd '$SOURCE' && timeout 60s kprove spec-labeled.k --definition '$PROOF_DEF' --spec-module SPEC-LABELED --trusted SPEC-LABELED.inner,SPEC-LABELED.outer"
entry_status=$?

printf 'SUMMARY concrete=%s all=%s inner=%s outer=%s entry=%s\n' \
  "$overall" "$all_claims_status" "$inner_status" "$outer_status" "$entry_status"
if [[ $overall -ne 0 || $all_claims_status -ne 0 || $inner_status -ne 0 || $outer_status -ne 0 || $entry_status -ne 0 ]]; then
  exit 1
fi
exit 0
