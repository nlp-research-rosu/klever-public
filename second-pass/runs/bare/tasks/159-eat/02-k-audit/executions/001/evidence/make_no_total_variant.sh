#!/usr/bin/env bash
set -eu

variant=/tmp/audit-work/159-eat/no-total
mkdir -p "$variant"
cp -a -- \
  /tmp/audit-work/159-eat/candidate-src/semantic.k \
  /tmp/audit-work/159-eat/candidate-src/verification.k \
  /tmp/audit-work/159-eat/candidate-src/spec.k \
  "$variant/"

# Mechanical audit mutation: retain every equation and remove only the
# over-broad totality attributes.
sed -i 's/[[]function, total[]]/[function]/g' "$variant/semantic.k"

printf 'REMOVED_TOTAL_ATTRIBUTES\n'
diff -u \
  /tmp/audit-work/159-eat/candidate-src/semantic.k \
  "$variant/semantic.k" || true
