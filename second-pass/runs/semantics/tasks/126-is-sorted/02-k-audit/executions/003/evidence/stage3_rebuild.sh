#!/usr/bin/env bash
set -u
set -o pipefail

WORK=/tmp/audit-work/126-is-sorted-audit-003
EVIDENCE=/audit-output/evidence

run_logged() {
  local label=$1
  shift
  local log="$EVIDENCE/$label.log"
  {
    printf '$'
    printf ' %q' "$@"
    printf '\n'
  } | tee "$log"
  timeout 600 "$@" 2>&1 | tee -a "$log"
  local command_status=${PIPESTATUS[0]}
  printf 'exit=%s\n' "$command_status" | tee -a "$log"
  return "$command_status"
}

cd "$WORK" || exit 98

for output in \
  audit-runtime-kompiled \
  audit-loop-verification-kompiled \
  audit-verification-kompiled
do
  if [[ -e "$output" ]]; then
    printf 'refusing to reuse existing build output: %s\n' "$output"
    exit 97
  fi
done

run_logged stage3_tool_versions kompile --version
run_logged stage3_runtime_build \
  kompile reference-semantics/semantics.k \
    --backend llvm \
    --main-module MPY-KRUN \
    --syntax-module MPY-SYNTAX \
    --output-definition audit-runtime-kompiled
run_logged stage3_runtime_solution \
  krun solution.mpy \
    --definition audit-runtime-kompiled \
    --output pretty

run_logged stage3_loop_build \
  kompile verification.k \
    --backend haskell \
    --main-module IS-SORTED-VERIFICATION \
    --syntax-module MPY-SYNTAX \
    --output-definition audit-loop-verification-kompiled
run_logged stage3_loop_proof \
  kprove spec.k \
    --definition audit-loop-verification-kompiled \
    --spec-module IS-SORTED-LOOP-SPEC \
    --output pretty

run_logged stage3_entry_build \
  kompile verification.k \
    --backend haskell \
    --main-module IS-SORTED-WITH-LOOP-LEMMA \
    --syntax-module MPY-SYNTAX \
    --output-definition audit-verification-kompiled
run_logged stage3_entry_proof \
  kprove spec.k \
    --definition audit-verification-kompiled \
    --spec-module IS-SORTED-SPEC \
    --output pretty
