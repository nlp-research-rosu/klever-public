#!/usr/bin/env bash
set -u
set -o pipefail

WORK=/tmp/audit-work/115-max-fill
VERIFICATION=/audit-output/evidence/05_body_mutation_verification.k
SPEC=/audit-output/evidence/05_body_mutation_spec.k
DEF="$WORK/body-mutation-kompiled"

cd "$WORK" || exit 125
printf 'MUTATION: loop-body numerator offset Int(1) -> Int(2)\n'
printf 'WITNESS: grid [[0]], capacity 1; original result 0, mutated result 1\n\n'

printf 'COMMAND: timeout 600s kompile %q -I %q --backend haskell --main-module MAX-FILL-VERIFICATION --syntax-module MPY-SYNTAX --output-definition %q\n' "$VERIFICATION" "$WORK" "$DEF"
timeout 600s kompile "$VERIFICATION" \
  -I "$WORK" \
  --backend haskell \
  --main-module MAX-FILL-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition "$DEF"
build_status=$?
printf 'EXIT_STATUS: %s\n\n' "$build_status"
if [[ "$build_status" -ne 0 ]]; then
  exit "$build_status"
fi

printf 'COMMAND: timeout 600s kprove %q -I %q --definition %q --spec-module MAX-FILL-SPEC\n' "$SPEC" "$WORK" "$DEF"
timeout 600s kprove "$SPEC" \
  -I "$WORK" \
  --definition "$DEF" \
  --spec-module MAX-FILL-SPEC
proof_status=$?
printf 'EXIT_STATUS: %s\n' "$proof_status"
if [[ "$proof_status" -eq 0 || "$proof_status" -eq 124 ]]; then
  exit 1
fi
exit 0
