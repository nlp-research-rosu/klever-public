#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/130-tri-audit
evidence=/audit-output/evidence
overall=0

run_logged() {
  name=$1
  shift
  log="$evidence/$name.full.log"
  printf '\nCOMMAND:'
  printf ' %q' "$@"
  printf '\nFULL_LOG: %s\n' "$log"
  "$@" >"$log" 2>&1
  status=$?
  printf 'EXIT_STATUS: %d\n' "$status"
  printf '%s\n' 'BOUNDED_OUTPUT_BEGIN'
  if [[ $(wc -l < "$log") -le 160 ]]; then
    sed -n '1,160p' "$log"
  else
    sed -n '1,80p' "$log"
    printf '%s\n' '... OUTPUT BOUNDED; FULL LOG PRESERVED ...'
    tail -n 80 "$log"
  fi
  printf '%s\n' 'BOUNDED_OUTPUT_END'
  if [[ "$status" -ne 0 ]]; then
    overall=1
  fi
  return 0
}

printf 'SCRATCH_PREBUILD_COMPILED_ARTIFACTS\n'
find "$scratch" \( -name '*-kompiled' -o -name '.kompile-*' -o -name '*.kore' \) -print

run_logged stage3_llvm_build \
  kompile "$scratch/reference-semantics/semantics.k" \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition "$scratch/runtime-audit-kompiled"

run_logged stage3_concrete_runtime \
  krun "$evidence/runtime_checks.mpy" \
  --definition "$scratch/runtime-audit-kompiled" \
  --output none

run_logged stage3_haskell_build \
  kompile "$scratch/verification.k" \
  --backend haskell \
  --main-module TRI-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition "$scratch/verification-audit-kompiled"

run_logged stage3_loop_claim \
  kprove "$scratch/spec.k" \
  --definition "$scratch/verification-audit-kompiled" \
  --spec-module TRI-LOOP-SPEC \
  --output pretty

run_logged stage3_entry_claim \
  kprove "$scratch/spec.k" \
  --definition "$scratch/verification-audit-kompiled" \
  --spec-module TRI-CORRECT-SPEC \
  --output pretty

for proof_log in "$evidence/stage3_loop_claim.full.log" "$evidence/stage3_entry_claim.full.log"; do
  top_count=$(grep -c '^#Top$' "$proof_log" || true)
  printf 'TOP_COUNT file=%s count=%s\n' "$proof_log" "$top_count"
  if [[ "$top_count" -ne 1 ]]; then
    overall=1
  fi
done

printf '\nSTAGE3_OVERALL_EXIT_STATUS: %d\n' "$overall"
exit "$overall"
