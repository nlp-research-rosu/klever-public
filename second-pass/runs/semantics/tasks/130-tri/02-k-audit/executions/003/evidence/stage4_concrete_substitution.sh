#!/usr/bin/env bash
set -uo pipefail

spec=/audit-output/evidence/stage4_concrete_substitution.k
definition=/tmp/audit-work/130-tri-audit/verification-audit-kompiled
log=/audit-output/evidence/stage4_concrete_substitution.full.log

printf 'COMMAND: kprove %q --definition %q --spec-module STAGE4-CONCRETE-SUBSTITUTION --output pretty\n' \
  "$spec" "$definition"
kprove "$spec" --definition "$definition" \
  --spec-module STAGE4-CONCRETE-SUBSTITUTION \
  --output pretty >"$log" 2>&1
status=$?
printf 'EXIT_STATUS: %d EXPECTED: 0\n' "$status"
sed -n '1,220p' "$log"
top_count=$(grep -c '^#Top$' "$log" || true)
printf 'TOP_COUNT: %s\n' "$top_count"
if [[ "$status" -ne 0 || "$top_count" -ne 1 ]]; then exit 1; fi
