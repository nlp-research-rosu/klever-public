#!/usr/bin/env bash
set -u

cd /tmp/audit-work/fresh || exit 90

echo '$ kast solution.mpy --definition verification-kompiled --module HOW-MANY-TIMES-VERIFICATION --sort Module --expand-macros --output kore --output-file solution-expanded.kore'
kast solution.mpy \
  --definition verification-kompiled \
  --module HOW-MANY-TIMES-VERIFICATION \
  --sort Module \
  --expand-macros \
  --output kore \
  --output-file solution-expanded.kore
solution_status=$?
echo "exit_status=$solution_status"

echo '$ kast claimed-program.mpy --definition verification-kompiled --module HOW-MANY-TIMES-VERIFICATION --sort Module --expand-macros --output kore --output-file claimed-expanded.kore'
kast claimed-program.mpy \
  --definition verification-kompiled \
  --module HOW-MANY-TIMES-VERIFICATION \
  --sort Module \
  --expand-macros \
  --output kore \
  --output-file claimed-expanded.kore
claimed_status=$?
echo "exit_status=$claimed_status"

echo '$ cmp solution-expanded.kore claimed-expanded.kore'
cmp solution-expanded.kore claimed-expanded.kore
cmp_status=$?
echo "exit_status=$cmp_status"

echo '$ sha256sum solution-expanded.kore claimed-expanded.kore'
sha256sum solution-expanded.kore claimed-expanded.kore
hash_status=$?
echo "exit_status=$hash_status"

if (( solution_status || claimed_status || cmp_status || hash_status )); then
  exit 1
fi
