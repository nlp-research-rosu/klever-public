#!/usr/bin/env bash
set -u

SCRATCH=/tmp/audit-work/anti-shuffle-audit
EVIDENCE=/audit-output/evidence
overall=0

run_proof() {
  name=$1
  shift
  output="$EVIDENCE/07_kprove_${name}.log"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@" > "$output" 2>&1
  status=$?
  top_count=$(grep -c '^#Top$' "$output" || true)
  printf 'EXIT: %d\n' "$status"
  printf 'TOP_LINES: %d\n' "$top_count"
  printf 'OUTPUT: %s\n\n' "$output"
  if [ "$status" -ne 0 ] || [ "$top_count" -lt 1 ]; then
    overall=1
  fi
}

run_proof insertion_loop \
  kprove "$SCRATCH/spec.k" \
  --definition "$SCRATCH/verification-kompiled" \
  --spec-module SPEC \
  --claims SPEC.insertion-loop

run_proof character_loop \
  kprove "$SCRATCH/spec.k" \
  --definition "$SCRATCH/verification-kompiled" \
  --spec-module SPEC \
  --claims SPEC.insertion-loop,SPEC.character-loop \
  --trusted SPEC.insertion-loop

run_proof entry \
  kprove "$SCRATCH/spec.k" \
  --definition "$SCRATCH/verification-kompiled" \
  --spec-module SPEC \
  --claims SPEC.insertion-loop,SPEC.character-loop,SPEC.anti-shuffle \
  --trusted SPEC.insertion-loop,SPEC.character-loop

exit "$overall"
