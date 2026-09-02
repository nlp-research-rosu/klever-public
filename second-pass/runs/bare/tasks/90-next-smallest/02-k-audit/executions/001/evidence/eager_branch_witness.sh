#!/usr/bin/env bash
set -uo pipefail

PROGRAM=/tmp/audit-work/90-next-smallest/source/solution.mpy
DEFINITION=/tmp/audit-work/90-next-smallest/rebuild/semantic-kompiled

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

printf 'The actual submitted program is run on the satisfying empty-list input.\n'
printf 'Depth 21 exposes evaluation of the then-subscript after false was computed.\n'
run krun "$PROGRAM" \
  --definition "$DEFINITION" \
  -cINPUT=nil \
  --depth 21 \
  --output pretty

printf 'Depth 27 exposes the fabricated invalidIndex sentinel in that untaken branch.\n'
run krun "$PROGRAM" \
  --definition "$DEFINITION" \
  -cINPUT=nil \
  --depth 27 \
  --output pretty
