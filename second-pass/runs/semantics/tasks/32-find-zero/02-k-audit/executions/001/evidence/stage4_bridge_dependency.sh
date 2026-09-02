#!/usr/bin/env bash
set +e

audit_source=/tmp/audit-work/32-find-zero/source

run() {
  printf '\nCOMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf 'EXIT_STATUS: %d\n' "$status"
  return "$status"
}

run cp /audit-output/evidence/verification_no_bridges.k "$audit_source/verification_no_bridges.k"
run cp /audit-output/evidence/no-bridge-return-spec.k "$audit_source/no-bridge-return-spec.k"

cd "$audit_source" || exit 98
printf 'WORKDIR: %s\n' "$PWD"

run kompile verification_no_bridges.k \
  --backend haskell \
  --main-module AUDIT-VERIFICATION-NO-BRIDGES \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-no-bridges-kompiled

run kprove no-bridge-return-spec.k \
  --definition audit-no-bridges-kompiled \
  --spec-module AUDIT-NO-BRIDGE-RETURN-SPEC

run sha256sum solution.mpy verification.k spec.k

run cp /audit-output/evidence/solution-body-mutation.mpy /tmp/audit-work/32-find-zero/solution-body-mutation.mpy
run cmp solution.mpy /tmp/audit-work/32-find-zero/solution-body-mutation.mpy
run sha256sum solution.mpy /tmp/audit-work/32-find-zero/solution-body-mutation.mpy

# The proof definition and spec have no dependency on either solution.mpy path.
run kprove positive-return-spec.k \
  --definition audit-verification-kompiled \
  --spec-module AUDIT-POSITIVE-RETURN-SPEC
