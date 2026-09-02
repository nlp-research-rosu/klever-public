#!/usr/bin/env bash
set -euo pipefail

work=/tmp/audit-work/reconstruction
definition="$work/verification-audit-kompiled"

printf '%s\n' \
  'COMMAND: kast solution.mpy --definition verification-audit-kompiled --module MPY-SYNTAX --sort Module --output kore'
kast "$work/solution.mpy" \
  --definition "$definition" \
  --module MPY-SYNTAX \
  --sort Module \
  --output kore >"$work/solution-parsed.kore"

printf '%s\n' \
  'COMMAND: kast spec-loaded-program.mpy --definition verification-audit-kompiled --module MPY-SYNTAX --sort Module --output kore'
kast "$work/spec-loaded-program.mpy" \
  --definition "$definition" \
  --module MPY-SYNTAX \
  --sort Module \
  --output kore >"$work/spec-loaded-program-parsed.kore"

printf '%s\n' \
  'COMMAND: cmp solution-parsed.kore spec-loaded-program-parsed.kore'
cmp "$work/solution-parsed.kore" "$work/spec-loaded-program-parsed.kore"
printf 'CMP_EXIT_STATUS: 0\n'
sha256sum "$work/solution-parsed.kore" "$work/spec-loaded-program-parsed.kore"
printf '%s\n' 'RESULT: submitted solution.mpy and the #loadAll program parse to identical KORE ASTs'
