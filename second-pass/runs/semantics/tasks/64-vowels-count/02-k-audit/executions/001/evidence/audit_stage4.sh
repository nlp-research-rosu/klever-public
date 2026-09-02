#!/usr/bin/env bash
set -u

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return 0
}

cd /tmp/audit-work/fresh || exit 1

run kast \
  --definition proof-base-kompiled \
  --module VOWELS-BASE \
  --sort Module \
  --expand-macros \
  --output kore \
  --output-file solution.parsed.kore \
  solution.mpy

run kast \
  --definition proof-base-kompiled \
  --module VOWELS-BASE \
  --sort Module \
  --expand-macros \
  --output kore \
  --output-file macro.parsed.kore \
  --expression vowelsModule

run cmp -s solution.parsed.kore macro.parsed.kore
run sha256sum solution.parsed.kore macro.parsed.kore

printf '$ python3 /reference/py2mpy.py ground_checks.py > ground_checks.mpy\n'
python3 /reference/py2mpy.py ground_checks.py > ground_checks.mpy
printf '[exit %d]\n' "$?"
run krun ground_checks.mpy --definition runtime-kompiled --output pretty
run python3 /audit-output/evidence/ground_values.py
