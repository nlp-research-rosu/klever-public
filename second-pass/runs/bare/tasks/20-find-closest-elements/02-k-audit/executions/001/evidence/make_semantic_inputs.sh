#!/usr/bin/env bash
set -euo pipefail

program=/tmp/audit-work/source/solution.mpy
destination=/tmp/audit-work/runtime-inputs
mkdir -p "$destination"

make_input() {
  local output=$1
  local value=$2
  {
    printf 'run(\n'
    sed 's/^/  /' "$program"
    printf ',\n  %s)\n' "$value"
  } >"$output"
}

make_input "$destination/example-six.run" \
  'vlist(vnum(1), vlist(vnum(2), vlist(vnum(3), vlist(vnum(4), vlist(vnum(5), vlist(vnum(11 /Rat 5), vnil))))))'
make_input "$destination/example-duplicate-six.run" \
  'vlist(vnum(1), vlist(vnum(2), vlist(vnum(3), vlist(vnum(4), vlist(vnum(5), vlist(vnum(2), vnil))))))'
make_input "$destination/boundary-ordered-two.run" \
  'vlist(vnum(1), vlist(vnum(2), vnil))'
make_input "$destination/boundary-reversed-two.run" \
  'vlist(vnum(2), vlist(vnum(1), vnil))'
make_input "$destination/boundary-duplicate-two.run" \
  'vlist(vnum(2), vlist(vnum(2), vnil))'
make_input "$destination/negative-four.run" \
  'vlist(vnum(-10), vlist(vnum(-3), vlist(vnum(-7 /Rat 2), vlist(vnum(9), vnil))))'
make_input "$destination/boundary-empty.run" 'vnil'

printf 'GENERATED_INPUTS:\n'
sha256sum "$destination"/*.run
