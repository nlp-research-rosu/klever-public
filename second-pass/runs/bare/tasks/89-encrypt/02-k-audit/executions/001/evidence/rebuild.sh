#!/usr/bin/env bash
set -u

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

source_dir=/tmp/audit-work/source
build_dir=/tmp/audit-work/build

cd "$source_dir" || exit 99

echo "K tool versions:"
run kompile --version || exit $?
run krun --version || exit $?
run kprove --version || exit $?

echo "Fresh LLVM concrete definition:"
run kompile semantic.k \
  --backend llvm \
  --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition "$build_dir/concrete-kompiled" || exit $?

echo "Fresh Haskell proof definition:"
run kompile semantic.k \
  --backend haskell \
  --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition "$build_dir/proof-kompiled" || exit $?

echo "Helper claim selected independently:"
run kprove spec.k \
  --definition "$build_dir/proof-kompiled" \
  --spec-module SPEC \
  --claims SPEC.encrypt-call-correct
call_status=$?

# program-correct depends on encrypt-call-correct. Selecting only
# SPEC.program-correct removes that circularity from the specification and is
# therefore not the target proof. The fresh diagnostic is separately preserved
# in program-only-diagnostic.log.
echo "All positive claims, including the dependent end-to-end claim:"
run kprove spec.k \
  --definition "$build_dir/proof-kompiled" \
  --spec-module SPEC
all_status=$?

printf 'summary helper=%d all=%d\n' "$call_status" "$all_status"

if (( call_status != 0 || all_status != 0 )); then
  exit 1
fi
exit 0
