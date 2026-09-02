#!/usr/bin/env bash
set -uo pipefail

work=/tmp/audit-work/137-compare-one-audit

if [[ ! -d "$work/concrete-kompiled" || ! -d "$work/proof-kompiled" ]]; then
  printf '%s\n' 'FAIL: fresh definitions from stage3_build_and_prove.log are absent'
  exit 1
fi

printf '%s\n' 'COMMAND: kast solution.mpy --output kore > solution-term.kore'
kast "$work/solution.mpy" \
  --definition "$work/proof-kompiled" \
  --module MPY-SYNTAX \
  --sort Pgm \
  --expand-macros \
  --output kore \
  > "$work/solution-term.kore"
status=$?
printf 'EXIT: %s\n' "$status"
(( status == 0 )) || exit "$status"

printf '%s\n' 'COMMAND: kast -e theSolution --output kore > proof-term.kore'
kast -e theSolution \
  --definition "$work/proof-kompiled" \
  --module VERIFICATION \
  --sort Pgm \
  --expand-macros \
  --output kore \
  > "$work/proof-term.kore"
status=$?
printf 'EXIT: %s\n' "$status"
(( status == 0 )) || exit "$status"

printf '%s\n' 'COMMAND: cmp solution-term.kore proof-term.kore'
cmp "$work/solution-term.kore" "$work/proof-term.kore"
status=$?
printf 'EXIT: %s\n' "$status"
(( status == 0 )) || exit "$status"
sha256sum "$work/solution-term.kore" "$work/proof-term.kore"

printf '%s\n' 'COMMAND: kprove spec.k --definition proof-kompiled --spec-module SPEC --output pretty'
kprove "$work/spec.k" \
  --definition "$work/proof-kompiled" \
  --spec-module SPEC \
  --output pretty
status=$?
printf 'EXIT: %s\n' "$status"
(( status == 0 )) || exit "$status"

printf '%s\n' 'STAGE3_AFTER_BUILD_OK'
