#!/usr/bin/env bash
set -u

work=/tmp/audit-work/87-get-row-review
cd "$work" || exit 1

run() {
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf 'EXIT: %d\n' "$status"
  return "$status"
}

run kompile verification-body-mutation.k \
  --main-module BODY-MUTATION-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --backend haskell \
  --output-definition body-mutation-kompiled || exit $?

printf '%s\n' \
  'COMMAND: kast --expression bodyMutatedProgram --definition body-mutation-kompiled --module BODY-MUTATION-VERIFICATION --sort Program --expand-macros --output kore > body-mutated-program.kore'
kast \
  --expression bodyMutatedProgram \
  --definition body-mutation-kompiled \
  --module BODY-MUTATION-VERIFICATION \
  --sort Program \
  --expand-macros \
  --output kore > body-mutated-program.kore
status=$?
printf 'EXIT: %d\n' "$status"
if [ "$status" -ne 0 ]; then exit "$status"; fi

run sha256sum parsed-program.kore body-mutated-program.kore || exit $?
if cmp -s parsed-program.kore body-mutated-program.kore; then
  printf '%s\n' 'ERROR: the body mutation did not change the executed program term'
  exit 1
fi
printf '%s\n' 'PROGRAM_TERM_CHANGED: true'

run python3 -c \
  'from solution import get_row; from trusted_canonical import get_row as c; x=([[],[0]],0); print("generated=",get_row(*x)); print("canonical=",c(*x))' \
  || exit $?

printf '%s\n' \
  'COMMAND: kprove spec-body-mutation.k --definition body-mutation-kompiled --spec-module SPEC-BODY-MUTATION --dry-run'
kprove spec-body-mutation.k \
  --definition body-mutation-kompiled \
  --spec-module SPEC-BODY-MUTATION \
  --dry-run
dry_status=$?
printf 'DRY-RUN EXIT: %d\n' "$dry_status"
if [ "$dry_status" -ne 0 ]; then exit 1; fi

printf '%s\n' \
  'COMMAND: kprove spec-body-mutation.k --definition body-mutation-kompiled --spec-module SPEC-BODY-MUTATION'
kprove spec-body-mutation.k \
  --definition body-mutation-kompiled \
  --spec-module SPEC-BODY-MUTATION \
  > body-mutation-proof.raw.log 2>&1
proof_status=$?
sed -n '1,240p' body-mutation-proof.raw.log
printf 'PROOF EXIT: %d\n' "$proof_status"
if [ "$proof_status" -eq 0 ]; then
  printf '%s\n' 'ERROR: the body mutation unexpectedly preserved the theorem'
  exit 1
fi
if ! rg -q 'WarnStuckClaimState|cannot be rewritten further|StuckClaim' \
  body-mutation-proof.raw.log; then
  printf '%s\n' 'ERROR: expected stuck-claim evidence was absent'
  exit 1
fi
printf '%s\n' 'BODY_SENSITIVITY_EXPECTED_FAILURE: true'
exit 0
