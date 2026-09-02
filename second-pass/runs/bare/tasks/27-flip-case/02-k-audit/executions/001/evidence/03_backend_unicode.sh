#!/usr/bin/env bash
set -u

program=/tmp/audit-work/candidate-src/solution.mpy

run_one() {
  backend=$1
  definition=$2
  spelling=$3
  karg=$4
  printf 'BACKEND=%s SPELLING=%s\n' "$backend" "$spelling"
  printf '$ krun %q --definition %q %q\n' "$program" "$definition" "-cARG=$karg"
  krun "$program" --definition "$definition" "-cARG=$karg"
  rc=$?
  printf '[exit %d]\n' "$rc"
}

for record in \
  'llvm|/tmp/audit-work/candidate-src/concrete-kompiled' \
  'haskell|/tmp/audit-work/candidate-src/proof-kompiled'
do
  backend=${record%%|*}
  definition=${record#*|}
  run_one "$backend" "$definition" unicode-escapes \
    '"Stra\u00dfe \u0394elta"'
  run_one "$backend" "$definition" utf8-byte-escapes \
    '"Stra\xc3\x9fe \xce\x94elta"'
  run_one "$backend" "$definition" raw-unicode \
    '"Straße Δelta"'
done
