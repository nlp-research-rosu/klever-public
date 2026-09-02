#!/usr/bin/env bash
set -u

SOURCE=/tmp/audit-work/source
PROOF_DEF=/tmp/audit-work/reconstruction/verification-haskell

run_shell() {
  local command_text="$1"
  printf 'COMMAND: %s\n' "$command_text"
  bash -o pipefail -c "$command_text"
  local status=$?
  printf 'EXIT_STATUS: %s\n\n' "$status"
  return "$status"
}

printf '%s\n' \
  'Each run leaves exactly one target claim untrusted.' \
  'Previously or separately proved helper claims remain available as trusted dependencies.' \
  'The inner claim has no helper; outer uses inner; entry uses inner and outer.'

run_shell "cd '$SOURCE' && timeout 60s kprove spec-labeled.k --definition '$PROOF_DEF' --spec-module SPEC-LABELED --exclude SPEC-LABELED.outer,SPEC-LABELED.entry"
inner_status=$?
run_shell "cd '$SOURCE' && timeout 60s kprove spec-labeled.k --definition '$PROOF_DEF' --spec-module SPEC-LABELED --exclude SPEC-LABELED.entry --trusted SPEC-LABELED.inner"
outer_status=$?
run_shell "cd '$SOURCE' && timeout 60s kprove spec-labeled.k --definition '$PROOF_DEF' --spec-module SPEC-LABELED --trusted SPEC-LABELED.inner,SPEC-LABELED.outer"
entry_status=$?

printf 'SUMMARY inner=%s outer=%s entry=%s\n' "$inner_status" "$outer_status" "$entry_status"
if [[ $inner_status -ne 0 || $outer_status -ne 0 || $entry_status -ne 0 ]]; then
  exit 1
fi
exit 0

