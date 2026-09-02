#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/114-minSubArraySum

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf '[exit %d]\n' "$status"
  return 0
}

cd "$scratch" || exit 1

run kast solution.mpy \
  --definition verification-base-kompiled \
  --module VERIFICATION-BASE \
  --sort Module \
  --expand-macros \
  --output kore \
  --output-file /tmp/audit-work/114-minSubArraySum/solution-expanded.kore

run kast macro-program.mpy \
  --definition verification-base-kompiled \
  --module VERIFICATION-BASE \
  --sort Module \
  --expand-macros \
  --output kore \
  --output-file /tmp/audit-work/114-minSubArraySum/macro-expanded.kore

run cmp -s solution-expanded.kore macro-expanded.kore
run sha256sum solution-expanded.kore macro-expanded.kore

run kprove ground-spec.k \
  --definition verification-kompiled \
  --spec-module GROUND-FUNCTION-SPEC \
  --output pretty

run python3 -c '
from canonical import minSubArraySum as canonical
from solution import minSubArraySum as candidate
cases = [[5], [-1, -2, -3], [2, 3, 4, 1, 2, 4]]
for xs in cases:
    print(xs, "canonical=", canonical(xs.copy()), "candidate=", candidate(xs.copy()))
'
