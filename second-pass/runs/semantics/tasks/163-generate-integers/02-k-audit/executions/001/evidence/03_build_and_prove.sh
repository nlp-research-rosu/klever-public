#!/usr/bin/env bash
set -u
set -o pipefail

work=/tmp/audit-work/submitted

run() {
  echo "CMD: $*"
  "$@"
  local status=$?
  echo "EXIT: $status"
  return "$status"
}

run kompile --version || exit $?
run kprove --version || exit $?

echo 'CMD: cmp -n 367 /candidate/solution.py /audit-output/evidence/03_concrete_audit.py'
cmp -n 367 /candidate/solution.py /audit-output/evidence/03_concrete_audit.py
status=$?
echo "EXIT: $status"
[[ $status -eq 0 ]] || exit "$status"

echo 'CMD: python3 /reference/py2mpy.py /audit-output/evidence/03_concrete_audit.py > /tmp/audit-work/submitted/03_concrete_audit.mpy'
python3 /reference/py2mpy.py \
  /audit-output/evidence/03_concrete_audit.py \
  > "$work/03_concrete_audit.mpy"
status=$?
echo "EXIT: $status"
[[ $status -eq 0 ]] || exit "$status"

run kompile "$work/reference-semantics/semantics.k" \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition "$work/runtime-kompiled" || exit $?

run krun "$work/03_concrete_audit.mpy" \
  --definition "$work/runtime-kompiled" || exit $?

run kompile "$work/verification.k" \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition "$work/verification-kompiled" || exit $?

echo 'CMD: rg -n "^[[:space:]]*claim\\b" /tmp/audit-work/submitted/spec.k /tmp/audit-work/submitted/verification.k'
rg -n '^[[:space:]]*claim\b' "$work/spec.k" "$work/verification.k"
status=$?
echo "EXIT: $status"
[[ $status -eq 0 ]] || exit "$status"

run kprove "$work/spec.k" \
  --definition "$work/verification-kompiled" \
  --spec-module SPEC \
  --smt-timeout 10000
