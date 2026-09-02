#!/usr/bin/env bash
set -uo pipefail

kast solution.regenerated.mpy \
  --definition audit-verification-kompiled \
  --module MPY-SYNTAX \
  --sort Module \
  --output kore > regenerated.kore
left_status=$?

kast pinned-solution.mpy \
  --definition audit-verification-kompiled \
  --module MPY-SYNTAX \
  --sort Module \
  --output kore > pinned.kore
right_status=$?

cmp -s regenerated.kore pinned.kore
cmp_status=$?

printf 'regenerated_kast_exit=%s\n' "$left_status"
printf 'pinned_kast_exit=%s\n' "$right_status"
printf 'constructor_kore_cmp_exit=%s\n' "$cmp_status"
sha256sum regenerated.kore pinned.kore

if [[ $left_status -ne 0 || $right_status -ne 0 || $cmp_status -ne 0 ]]; then
  exit 1
fi
