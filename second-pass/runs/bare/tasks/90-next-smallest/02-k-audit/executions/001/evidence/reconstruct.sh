#!/usr/bin/env bash
set -uo pipefail

SOURCE=/tmp/audit-work/90-next-smallest/source
REBUILD=/tmp/audit-work/90-next-smallest/rebuild
SEMANTIC_DEF="$REBUILD/semantic-kompiled"
VERIFICATION_DEF="$REBUILD/verification-kompiled"

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

run mkdir -p "$REBUILD" || exit $?
run test ! -e "$SEMANTIC_DEF" || exit $?
run test ! -e "$VERIFICATION_DEF" || exit $?
run kompile --version || exit $?
run kprove --version || exit $?

run kompile "$SOURCE/semantic.k" \
  --backend llvm \
  --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --output-definition "$SEMANTIC_DEF" || exit $?

run python3 /audit-output/evidence/concrete_compare.py \
  "$SOURCE/solution.mpy" \
  "$SEMANTIC_DEF" \
  "$SOURCE/canonical.py" \
  "$SOURCE/solution.py" \
  /audit-output/evidence/concrete-results.json || exit $?

run kompile "$SOURCE/verification.k" \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition "$VERIFICATION_DEF" || exit $?

run kprove "$SOURCE/spec.k" \
  --definition "$VERIFICATION_DEF" \
  --spec-module SPEC \
  --claims next-smallest-correct \
  --output pretty
proof_status=$?
printf 'positive_claim_status=%d\n' "$proof_status"
exit "$proof_status"
