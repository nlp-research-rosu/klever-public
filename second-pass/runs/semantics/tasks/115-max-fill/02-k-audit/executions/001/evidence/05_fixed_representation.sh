#!/usr/bin/env bash
set -u
set -o pipefail

WORK=/tmp/audit-work/115-max-fill
SOURCE=/audit-output/evidence/05_fixed_representation.k
DEF="$WORK/fixed-representation-kompiled"
overall=0

run() {
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf 'EXIT_STATUS: %s\n\n' "$status"
  if [[ "$status" -ne 0 ]]; then
    overall=1
  fi
  return 0
}

cd "$WORK" || exit 125
run timeout 600s kompile "$SOURCE" \
  -I "$WORK" \
  --backend haskell \
  --main-module MAX-FILL-FIXED-REPRESENTATION \
  --syntax-module MPY-SYNTAX \
  --output-definition "$DEF"
run timeout 600s kprove "$SOURCE" \
  -I "$WORK" \
  --definition "$DEF" \
  --spec-module MAX-FILL-FIXED-REPRESENTATION-SPEC
exit "$overall"
