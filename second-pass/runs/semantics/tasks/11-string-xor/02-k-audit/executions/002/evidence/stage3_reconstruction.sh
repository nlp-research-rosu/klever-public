#!/usr/bin/env bash
set -uo pipefail

work=/tmp/audit-work/11-string-xor/candidate
runtime_definition="$work/audit-runtime-kompiled"
proof_definition="$work/audit-verification-kompiled"

run() {
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf 'EXIT_STATUS: %s\n' "$status"
  return "$status"
}

run command -v kompile
status=$?
[ "$status" -eq 0 ] || exit "$status"
run command -v krun
status=$?
[ "$status" -eq 0 ] || exit "$status"
run command -v kprove
status=$?
[ "$status" -eq 0 ] || exit "$status"
run kompile --version
status=$?
[ "$status" -eq 0 ] || exit "$status"
run kprove --version
status=$?
[ "$status" -eq 0 ] || exit "$status"

printf 'COMMAND: test ! -e %q -a ! -e %q\n' "$runtime_definition" "$proof_definition"
test ! -e "$runtime_definition" -a ! -e "$proof_definition"
status=$?
printf 'EXIT_STATUS: %s\n' "$status"
[ "$status" -eq 0 ] || exit "$status"

cd "$work" || exit 1

run kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition "$runtime_definition"
status=$?
[ "$status" -eq 0 ] || exit "$status"

run krun concrete_tests.mpy --definition "$runtime_definition"
status=$?
[ "$status" -eq 0 ] || exit "$status"

run kompile verification.k \
  --backend haskell \
  --main-module STRING-XOR-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition "$proof_definition"
status=$?
[ "$status" -eq 0 ] || exit "$status"

run kprove spec.k \
  --definition "$proof_definition" \
  --spec-module STRING-XOR-SPEC \
  --claims STRING-XOR-SPEC.loop-invariant
loop_status=$?

run timeout 300 kprove spec.k \
  --definition "$proof_definition" \
  --spec-module STRING-XOR-SPEC \
  --claims STRING-XOR-SPEC.loop-invariant,STRING-XOR-SPEC.solution-correct
all_claims_status=$?

printf 'POSITIVE_STATUS loop-invariant-alone=%s all-claims-including-solution-correct=%s\n' \
  "$loop_status" "$all_claims_status"
[ "$loop_status" -eq 0 ] && [ "$all_claims_status" -eq 0 ]
exit $?
