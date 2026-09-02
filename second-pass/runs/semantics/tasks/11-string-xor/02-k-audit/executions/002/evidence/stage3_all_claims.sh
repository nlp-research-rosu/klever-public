#!/usr/bin/env bash
set -uo pipefail

work=/tmp/audit-work/11-string-xor/candidate
proof_definition="$work/audit-verification-kompiled"
cd "$work" || exit 1

printf 'COMMAND: timeout 300 kprove spec.k --definition %q --spec-module STRING-XOR-SPEC --claims STRING-XOR-SPEC.loop-invariant,STRING-XOR-SPEC.solution-correct\n' \
  "$proof_definition"
timeout 300 kprove spec.k \
  --definition "$proof_definition" \
  --spec-module STRING-XOR-SPEC \
  --claims STRING-XOR-SPEC.loop-invariant,STRING-XOR-SPEC.solution-correct
status=$?
printf 'EXIT_STATUS: %s\n' "$status"
exit "$status"
