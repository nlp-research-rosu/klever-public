#!/usr/bin/env bash
set +e

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return 0
}

SCRATCH=/tmp/audit-work/candidate
SPEC="$SCRATCH/audit-spec-labeled.k"
DEF="$SCRATCH/verification-kompiled"

printf '%s\n' 'Per-target runs with required circularity dependency closures'
printf '%s\n' 'loop-empty: no helper claim'
run kprove "$SPEC" --definition "$DEF" --spec-module AUDIT-SPEC-LABELED \
  --claims AUDIT-SPEC-LABELED.loop-empty

printf '%s\n' 'loop-rest: self-circular recurrent-loop claim'
run kprove "$SPEC" --definition "$DEF" --spec-module AUDIT-SPEC-LABELED \
  --claims AUDIT-SPEC-LABELED.loop-rest

printf '%s\n' 'loop-first: requires recurrent-loop circularity'
run kprove "$SPEC" --definition "$DEF" --spec-module AUDIT-SPEC-LABELED \
  --claims AUDIT-SPEC-LABELED.loop-first,AUDIT-SPEC-LABELED.loop-rest

printf '%s\n' 'entry: requires all three loop claims'
run kprove "$SPEC" --definition "$DEF" --spec-module AUDIT-SPEC-LABELED \
  --claims AUDIT-SPEC-LABELED.loop-empty,AUDIT-SPEC-LABELED.loop-first,AUDIT-SPEC-LABELED.loop-rest,AUDIT-SPEC-LABELED.entry
