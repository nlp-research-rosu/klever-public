#!/usr/bin/env bash
set -u

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

overall=0

run python3 /audit-output/evidence/semantic_scope_witness.py || overall=1

# Witness that the slice sentinel is over-broad: direct integer index 1 is
# incorrectly interpreted as a tail slice by the generated semantics.
run krun /audit-output/evidence/direct-index-one.mpy \
  --definition /tmp/audit-work/build/semantic-llvm-r2 \
  '-cINPUT=VList(10 ; 20 ; 30 ; .Ints)' \
  --output pretty || overall=1

# Witness that an empty function body returns K false, whereas CPython returns
# None. The submitted functions never reach this rule.
run krun /audit-output/evidence/fallthrough.mpy \
  --definition /tmp/audit-work/build/semantic-llvm-r2 \
  '-cINPUT=VList(10 ; 20 ; 30 ; .Ints)' \
  --output pretty || overall=1

# Ground operational-context checks: helper/entry results flow into `finish`
# and update the observable result cell rather than discarding the continuation.
run kprove /audit-output/evidence/context-check.k \
  --definition /tmp/audit-work/build/verification-haskell-r2 \
  --spec-module AUDIT-CONTEXT-CHECK \
  --output pretty || overall=1

run kast \
  --definition /tmp/audit-work/build/verification-haskell-r2 \
  --module MPY-SYNTAX \
  --sort Program \
  --input program \
  --output kore \
  --output-file /tmp/audit-work/solution-mutated.kore \
  /audit-output/evidence/solution-mutated.mpy || overall=1

printf '\n$ cmp -s /tmp/audit-work/submitted-solution.kore /tmp/audit-work/solution-mutated.kore\n'
cmp -s \
  /tmp/audit-work/submitted-solution.kore \
  /tmp/audit-work/solution-mutated.kore
status=$?
printf '[exit %d; expected nonzero because the body mutation must break the source-tree pin]\n' "$status"
if (( status == 0 )); then
  overall=1
fi

run krun /audit-output/evidence/solution-mutated.mpy \
  --definition /tmp/audit-work/build/semantic-llvm-r2 \
  '-cINPUT=VList(0 ; 0 ; 0 ; .Ints)' \
  --output pretty || overall=1

printf '\n[script exit %d]\n' "$overall"
exit "$overall"
