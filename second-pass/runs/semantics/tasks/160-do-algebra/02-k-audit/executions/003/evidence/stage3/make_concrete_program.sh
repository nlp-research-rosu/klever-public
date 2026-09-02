#!/usr/bin/env bash
set -euo pipefail

if (( $# != 2 )); then
  echo "usage: $0 OUTPUT_MPY EXPRESSION_TERM" >&2
  exit 64
fi

output=$1
expression=$2
source=/tmp/audit-work/160-do-algebra/solution.mpy

sed '$ s/)$//' "$source" >"$output"
printf '  Expr(%s)\n' "$expression" >>"$output"
printf ')\n' >>"$output"
