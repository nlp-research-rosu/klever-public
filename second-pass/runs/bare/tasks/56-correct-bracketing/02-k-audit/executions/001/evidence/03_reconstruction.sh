#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/reconstruction/candidate-src
llvm_def=/tmp/audit-work/reconstruction/fresh-llvm-kompiled
haskell_def=/tmp/audit-work/reconstruction/fresh-haskell-kompiled
failed=0

run_checked() {
  local description="$1"
  shift
  echo "AUDITOR COMMAND ($description):"
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  echo "EXIT STATUS: $status"
  if (( status != 0 )); then
    failed=1
  fi
  return 0
}

cd "$scratch" || exit 2

run_checked 'fresh LLVM build from source' \
  kompile semantic.k \
    --backend llvm \
    --main-module MPY \
    --syntax-module MPY-SYNTAX \
    --output-definition "$llvm_def"

run_checked 'fresh Haskell proof build from source' \
  kompile semantic.k \
    --backend haskell \
    --main-module MPY \
    --syntax-module MPY-SYNTAX \
    --output-definition "$haskell_def"

for input in '""' '"<"' '"<>"' '">"' '"><"' '"<<>>"' '"<>>"' '"<<><>>"'
do
  run_checked "fresh concrete semantics, INPUT=$input" \
    krun solution.mpy --definition "$llvm_def" -cINPUT="$input"
done

run_checked 'all original candidate claims together' \
  kprove spec.k \
    --definition "$haskell_def" \
    --spec-module SPEC

# The two loop claims are a mutually recursive invariant SCC and therefore must
# be selected together.  The universal entry claim depends on that SCC.
run_checked 'mutually dependent loop-zero and loop-positive claims' \
  kprove audit-spec.k \
    --definition "$haskell_def" \
    --spec-module AUDIT-SPEC \
    --claims AUDIT-SPEC.loop-zero,AUDIT-SPEC.loop-positive

run_checked 'universal entry claim with its two invariant dependencies' \
  kprove audit-spec.k \
    --definition "$haskell_def" \
    --spec-module AUDIT-SPEC \
    --claims AUDIT-SPEC.loop-zero,AUDIT-SPEC.loop-positive,AUDIT-SPEC.universal-correctness

for label in example-open example-pair example-nested example-negative-prefix
do
  run_checked "individual concrete claim $label" \
    kprove audit-spec.k \
      --definition "$haskell_def" \
      --spec-module AUDIT-SPEC \
      --claims "AUDIT-SPEC.$label"
done

echo "AGGREGATE FAILURE FLAG: $failed"
exit "$failed"
