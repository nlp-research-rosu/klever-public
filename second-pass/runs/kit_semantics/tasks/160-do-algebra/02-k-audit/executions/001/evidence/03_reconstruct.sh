#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/160-do-algebra
runtime="$scratch/audit-runtime-kompiled"
proof_definition="$scratch/audit-verification-kompiled"

run_logged() {
  local label=$1
  shift
  local log="/audit-output/evidence/${label}.log"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  {
    printf 'COMMAND:'
    printf ' %q' "$@"
    printf '\n'
  } > "$log"
  "$@" 2>&1 | tee -a "$log"
  local status=${PIPESTATUS[0]}
  printf 'EXIT_STATUS=%d\n' "$status" | tee -a "$log"
  return "$status"
}

if [[ -e "$runtime" || -e "$proof_definition" ]]; then
  echo "ERROR: reviewer definition already exists; refusing to reuse a cache"
  exit 90
fi

cp /audit-output/evidence/fixtures/k_concrete_cases.py "$scratch/k_concrete_cases.py"
cp /audit-output/evidence/fixtures/k_zero_divisor.py "$scratch/k_zero_divisor.py"

(
  cd "$scratch" || exit 91
  python3 py2mpy.py k_concrete_cases.py > k_concrete_cases.mpy
  python3 py2mpy.py k_zero_divisor.py > k_zero_divisor.mpy
)
translate_status=$?
echo "TRANSLATOR_EXIT_STATUS=$translate_status"
if (( translate_status != 0 )); then
  exit "$translate_status"
fi

run_logged 03a_kompile_llvm \
  kompile "$scratch/reference-semantics/semantics.k" \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition "$runtime" || exit $?

run_logged 03b_krun_concrete \
  krun "$scratch/k_concrete_cases.mpy" \
  --definition "$runtime" || exit $?

run_logged 03c_kompile_haskell \
  kompile "$scratch/verification.k" \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition "$proof_definition" || exit $?

run_logged 03d_kprove_algebra_loop \
  kprove "$scratch/spec.k" \
  --definition "$proof_definition" \
  --spec-module SPEC \
  --claims SPEC.algebra-loop || exit $?

run_logged 03e_kprove_do_algebra \
  kprove "$scratch/spec.k" \
  --definition "$proof_definition" \
  --spec-module SPEC \
  --claims SPEC.do-algebra || exit $?

run_logged 03f_kprove_all \
  kprove "$scratch/spec.k" \
  --definition "$proof_definition" \
  --spec-module SPEC || exit $?

echo "RESULT: PASS"
